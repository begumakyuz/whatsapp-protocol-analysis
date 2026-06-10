import pytest
import math
from src.core.protobuf import WhatsAppProtobufDecoder
from src.core.parser import calculate_shannon_entropy
from src.core.crypto_handshake import WhatsAppNoiseHandshakeSimulator

# --- SHANNON ENTROPY TESTS ---
def test_shannon_entropy_pure_plaintext():
    text_data = b"AAAAAAAABBBBBBBB"
    entropy = calculate_shannon_entropy(text_data)
    assert entropy == 1.0

def test_shannon_entropy_high_randomness():
    random_data = b"\x8f\x12\x9a\xf4\x33\xbc\xde\x11\x04\x6a"
    entropy = calculate_shannon_entropy(random_data)
    assert entropy > 2.0

# --- PROTOBUF DECODER TESTS ---
def test_protobuf_wire_type_parsing():
    field_num, wire_type = WhatsAppProtobufDecoder.parse_wire_type(0x0A) # tag = 10 (field 1, wire 2)
    assert field_num == 1
    assert wire_type == 2

def test_protobuf_varint_decoder_valid():
    varint_bytes = b"\x96\x01" # 150 sayısının varint karşılığı
    value, read_bytes = WhatsAppProtobufDecoder.decode_varint(varint_bytes, 0)
    assert value == 150
    assert read_bytes == 2

def test_protobuf_varint_decoder_zero():
    value, read_bytes = WhatsAppProtobufDecoder.decode_varint(b"\x00", 0)
    assert value == 0
    assert read_bytes == 1

# --- HANDSHAKE & FSM SIMULATOR TESTS ---
def test_crypto_handshake_initial_state():
    simulator = WhatsAppNoiseHandshakeSimulator()
    assert simulator.current_state == "INIT"

def test_crypto_handshake_state_transitions():
    simulator = WhatsAppNoiseHandshakeSimulator()
    
    # INIT -> NOISE_HANDSHAKE_SENT
    success_1 = simulator.track_fsm_state("NOISE_HANDSHAKE_SENT")
    assert success_1 is True
    assert simulator.current_state == "NOISE_HANDSHAKE_SENT"
    
    # NOISE_HANDSHAKE_SENT -> HANDSHAKE_COMPLETED
    success_2 = simulator.track_fsm_state("HANDSHAKE_COMPLETED")
    assert success_2 is True
    assert simulator.current_state == "HANDSHAKE_COMPLETED"

def test_crypto_handshake_invalid_transition():
    simulator = WhatsAppNoiseHandshakeSimulator()
    # INIT aşamasından doğrudan COMPLETED aşamasına zıplanamaz (FSM kuralı)
    success = simulator.track_fsm_state("HANDSHAKE_COMPLETED")
    assert success is False