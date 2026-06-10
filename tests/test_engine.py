import pytest
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
# pyrefly: ignore [missing-import]
from core.protobuf import WhatsAppProtobufDecoder
from core.parser import CryptographicAnalyzer
from core.crypto_handshake import WhatsAppNoiseHandshakeSimulator

# --- SHANNON ENTROPY TESTS ---
def test_shannon_entropy_pure_plaintext():
    text_data = b"AAAAAAAABBBBBBBB"
    entropy = CryptographicAnalyzer.calculate_shannon_entropy(text_data)
    assert entropy == 1.0

def test_shannon_entropy_high_randomness():
    random_data = b"\x8f\x12\x9a\xf4\x33\xbc\xde\x11\x04\x6a"
    entropy = CryptographicAnalyzer.calculate_shannon_entropy(random_data)
    assert entropy > 2.0

def test_shannon_entropy_type_error():
    with pytest.raises(TypeError):
        CryptographicAnalyzer.calculate_shannon_entropy(123) # type: ignore

# --- PROTOBUF DECODER TESTS ---
def test_protobuf_parse_raw_valid():
    # Field 1, wire type 0 (varint), value 150
    # Tag: (1 << 3) | 0 = 8. 150 as varint: 0x96 0x01
    raw_bytes = b"\x08\x96\x01"
    decoder = WhatsAppProtobufDecoder()
    fields = decoder.parse_raw_protobuf(raw_bytes)
    assert 1 in fields
    assert fields[1]["type"] == "Varint"
    assert fields[1]["value"] == 150

def test_protobuf_varint_decoder_valid():
    varint_bytes = b"\x96\x01" # 150 sayısının varint karşılığı
    value, read_bytes = WhatsAppProtobufDecoder.decode_varint(varint_bytes, 0)
    assert value == 150
    assert read_bytes == 2

def test_protobuf_varint_decoder_zero():
    value, read_bytes = WhatsAppProtobufDecoder.decode_varint(b"\x00", 0)
    assert value == 0
    assert read_bytes == 1

def test_protobuf_varint_dos_protection():
    # Çok uzun, asla sonlanmayan (hep 0x80 bitli) bir varint dizisi
    malicious_bytes = b"\x80" * 15
    with pytest.raises(ValueError, match="Maksimum Varint boyutu aşıldı"):
        WhatsAppProtobufDecoder.decode_varint(malicious_bytes, 0)

# --- HANDSHAKE & FSM SIMULATOR TESTS ---
def test_crypto_handshake_initial_state():
    simulator = WhatsAppNoiseHandshakeSimulator()
    assert simulator.handshake_phase == "EPHEMERAL_EXCHANGE"

def test_crypto_handshake_state_transitions():
    simulator = WhatsAppNoiseHandshakeSimulator()
    
    # EPHEMERAL_EXCHANGE -> SERVER_RESPONSE_WAIT (is_outgoing=True)
    dummy_payload = b"A" * 32
    success_1 = simulator.process_handshake_step(dummy_payload, is_outgoing=True)
    assert success_1 is True
    assert simulator.handshake_phase == "SERVER_RESPONSE_WAIT"
    
    # SERVER_RESPONSE_WAIT -> CLIENT_FINAL_SIGN (is_outgoing=False)
    success_2 = simulator.process_handshake_step(dummy_payload, is_outgoing=False)
    assert success_2 is True
    assert simulator.handshake_phase == "CLIENT_FINAL_SIGN"

def test_crypto_handshake_invalid_transition():
    simulator = WhatsAppNoiseHandshakeSimulator()
    # Sunucu daha en başta yanıt veremez
    dummy_payload = b"A" * 32
    success = simulator.process_handshake_step(dummy_payload, is_outgoing=False)
    assert success is False