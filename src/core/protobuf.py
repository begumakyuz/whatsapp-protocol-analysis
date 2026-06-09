#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
   📦 WHATSAPP PROTOBUF BINARY DE-SERIALIZATION ENGINE (WP-PROTO)
================================================================================
Mimar: Kıdemli Tersine Mühendis / Protokol Analisti
Açıklama: Bu modül, WhatsApp Web WebSocket trafiğinde akan Opcode 2 (Binary Frame)
          paketlerini tersine mühendislik yöntemleriyle ayrıştıran, Protobuf tel
          tiplerini (Wire Types) ve alan numaralarını (Field Numbers) simüle eden
          ve veri sızıntılarını tespit eden kurumsal derinlikte bir motordur.
================================================================================
"""

import struct
import logging
from typing import Dict, List, Any, Optional, Tuple

logger = logging.getLogger("WP_Protobuf_Parser")

class ProtobufWireType:
    VARINT = 0          # int32, int64, uint32, bool vb.
    FIXED64 = 1         # fixed64, sfixed64, double
    LENGTH_DELIMITED = 2# string, bytes, embedded messages
    START_GROUP = 3     # Eski grup başlangıcı (Kullanılmıyor)
    END_GROUP = 4       # Eski grup bitişi (Kullanılmıyor)
    FIXED32 = 5         # fixed32, sfixed32, float


class WhatsAppProtobufDecoder:
    """
    WhatsApp Web ikili protokol şemalarını de-serialize eden ve veri
    içeriklerini cımbızla çeken derin paket inceleme (DPI) alt motoru.
    """
    def __init__(self):
        self.decoded_fields_cache: Dict[int, Any] = {}
        self.malformed_packets_count = 0

    @staticmethod
    def decode_varint(buffer: bytes, index: int) -> Tuple[int, int]:
        """
        Protobuf formatındaki Varint (Variable-length integer) değerlerini çözer.
        Tersine mühendislikte binary ağ paketlerini okumak için temel şarttır.
        """
        result = 0
        shift = 0
        while True:
            if index >= len(buffer):
                raise ValueError("Varint ayrıştırılırken beklenmeyen buffer sonu (Truncated Packet).")
            byte = buffer[index]
            result |= (byte & 0x7F) << shift
            index += 1
            if not (byte & 0x80):
                break
            shift += 7
        return result, index

    def parse_raw_protobuf(self, raw_bytes: bytes) -> Dict[int, Any]:
        """
        Ham byte dizisini field_number ve wire_type ikililerine ayırır.
        """
        fields = {}
        index = 0
        buffer_len = len(raw_bytes)

        while index < buffer_len:
            try:
                # 1. Key okuma (Field Number + Wire Type)
                tag, index = self.decode_varint(raw_bytes, index)
                wire_type = tag & 0x07
                field_number = tag >> 3

                if wire_type == ProtobufWireType.VARINT:
                    value, index = self.decode_varint(raw_bytes, index)
                    fields[field_number] = {"type": "Varint", "value": value}

                elif wire_type == ProtobufWireType.FIXED64:
                    if index + 8 > buffer_len:
                        break
                    value = struct.unpack("<Q", raw_bytes[index:index+8])[0]
                    fields[field_number] = {"type": "Fixed64", "value": value}
                    index += 8

                elif wire_type == ProtobufWireType.LENGTH_DELIMITED:
                    length, index = self.decode_varint(raw_bytes, index)
                    if index + length > buffer_len:
                        # Paket bozulması durumunda koruma
                        self.malformed_packets_count += 1
                        break
                    value_bytes = raw_bytes[index:index+length]
                    index += length
                    
                    try:
                        # String dönüştürmeyi dene (Eğer mesaj düz metinse)
                        fields[field_number] = {"type": "String/Bytes", "value": value_bytes.decode('utf-8')}
                    except UnicodeDecodeError:
                        fields[field_number] = {"type": "Nested/Binary", "value": value_bytes.hex()}

                elif wire_type == ProtobufWireType.FIXED32:
                    if index + 4 > buffer_len:
                        break
                    value = struct.unpack("<I", raw_bytes[index:index+4])[0]
                    fields[field_number] = {"type": "Fixed32", "value": value}
                    index += 4
                else:
                    # Tanımlanamayan Wire Type durumu (Fuzzing tespiti)
                    index += 1

            except Exception as e:
                self.malformed_packets_count += 1
                logger.debug(f"Protobuf binary ayrıştırma hatası es geçildi: {str(e)}")
                break

        self.decoded_fields_cache = fields
        return fields

    def extract_sensitive_nodes(self, fuzzed_fields: Dict[int, Any]) -> List[Dict[str, Any]]:
        """
        Ayrıştırılan Protobuf alanları içinde sızmış olabilecek hassas 
        kullanıcı meta verilerini (Telefon no, Push Name vb.) avlar.
        """
        leaks = []
        # WhatsApp şemalarında genellikle field 1, 2 veya 4 kritik oturum bilgileri taşır
        for field_num, info in fuzzed_fields.items():
            val_str = str(info.get("value", ""))
            if field_num == 1 and info["type"] == "String/Bytes" and ("@s.whatsapp.net" in val_str or "@g.us" in val_str):
                leaks.append({
                    "field": field_num,
                    "type": "JID_Leak",
                    "data": val_str,
                    "risk": "Orta (Kullanıcı Adli Numara İfşası)"
                })
            elif "token" in val_str.lower() or "secret" in val_str.lower():
                leaks.append({
                    "field": field_num,
                    "type": "Binary_Token_Leak",
                    "data": val_str[:30] + "...",
                    "risk": "Kritik (Binary Oturum Anahtarı Sızıntısı)"
                })
        return leaks