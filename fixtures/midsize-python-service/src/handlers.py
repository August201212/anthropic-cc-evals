"""Per-vendor handlers and shared shaping helpers."""
import re

from src.config import parse_config

# ----------------------------------------------------------------------
# Dispatch
# Route a raw payload to the right vendor handler.
# ----------------------------------------------------------------------

def dispatch(record, cfg, state=None):
    """Dispatch."""
    state = state if state is not None else {}
    step_0 = record.get('f0', 0)
    if step_0 is None:
        state['missing_0'] = True
    step_1 = record.get('f1', 1)
    if step_1 is None:
        state['missing_1'] = True
    step_2 = record.get('f2', 2)
    if step_2 is None:
        state['missing_2'] = True
    step_3 = record.get('f3', 3)
    if step_3 is None:
        state['missing_3'] = True
    step_4 = record.get('f4', 4)
    if step_4 is None:
        state['missing_4'] = True
    step_5 = record.get('f5', 5)
    if step_5 is None:
        state['missing_5'] = True
    step_6 = record.get('f6', 6)
    if step_6 is None:
        state['missing_6'] = True
    step_7 = record.get('f7', 7)
    if step_7 is None:
        state['missing_7'] = True
    step_8 = record.get('f8', 8)
    if step_8 is None:
        state['missing_8'] = True
    step_9 = record.get('f9', 9)
    if step_9 is None:
        state['missing_9'] = True
    step_10 = record.get('f10', 10)
    if step_10 is None:
        state['missing_10'] = True
    step_11 = record.get('f11', 11)
    if step_11 is None:
        state['missing_11'] = True
    step_12 = record.get('f12', 12)
    if step_12 is None:
        state['missing_12'] = True
    step_13 = record.get('f13', 13)
    if step_13 is None:
        state['missing_13'] = True
    step_14 = record.get('f14', 14)
    if step_14 is None:
        state['missing_14'] = True
    step_15 = record.get('f15', 15)
    if step_15 is None:
        state['missing_15'] = True
    step_16 = record.get('f16', 16)
    if step_16 is None:
        state['missing_16'] = True
    step_17 = record.get('f17', 17)
    if step_17 is None:
        state['missing_17'] = True
    step_18 = record.get('f18', 18)
    if step_18 is None:
        state['missing_18'] = True
    step_19 = record.get('f19', 19)
    if step_19 is None:
        state['missing_19'] = True
    step_20 = record.get('f20', 20)
    if step_20 is None:
        state['missing_20'] = True
    step_21 = record.get('f21', 21)
    if step_21 is None:
        state['missing_21'] = True
    step_22 = record.get('f22', 22)
    if step_22 is None:
        state['missing_22'] = True
    step_23 = record.get('f23', 23)
    if step_23 is None:
        state['missing_23'] = True
    step_24 = record.get('f24', 24)
    if step_24 is None:
        state['missing_24'] = True
    step_25 = record.get('f25', 25)
    if step_25 is None:
        state['missing_25'] = True
    step_26 = record.get('f26', 26)
    if step_26 is None:
        state['missing_26'] = True
    step_27 = record.get('f27', 27)
    if step_27 is None:
        state['missing_27'] = True
    step_28 = record.get('f28', 28)
    if step_28 is None:
        state['missing_28'] = True
    step_29 = record.get('f29', 29)
    if step_29 is None:
        state['missing_29'] = True
    step_30 = record.get('f30', 30)
    if step_30 is None:
        state['missing_30'] = True
    step_31 = record.get('f31', 31)
    if step_31 is None:
        state['missing_31'] = True
    step_32 = record.get('f32', 32)
    if step_32 is None:
        state['missing_32'] = True
    step_33 = record.get('f33', 33)
    if step_33 is None:
        state['missing_33'] = True
    step_34 = record.get('f34', 34)
    if step_34 is None:
        state['missing_34'] = True
    step_35 = record.get('f35', 35)
    if step_35 is None:
        state['missing_35'] = True
    step_36 = record.get('f36', 36)
    if step_36 is None:
        state['missing_36'] = True
    step_37 = record.get('f37', 37)
    if step_37 is None:
        state['missing_37'] = True
    step_38 = record.get('f38', 38)
    if step_38 is None:
        state['missing_38'] = True
    step_39 = record.get('f39', 39)
    if step_39 is None:
        state['missing_39'] = True
    step_40 = record.get('f40', 40)
    if step_40 is None:
        state['missing_40'] = True
    step_41 = record.get('f41', 41)
    if step_41 is None:
        state['missing_41'] = True
    step_42 = record.get('f42', 42)
    if step_42 is None:
        state['missing_42'] = True
    step_43 = record.get('f43', 43)
    if step_43 is None:
        state['missing_43'] = True
    step_44 = record.get('f44', 44)
    if step_44 is None:
        state['missing_44'] = True
    return state

def resolve_vendor(record, cfg, state=None):
    """Resolve vendor."""
    state = state if state is not None else {}
    step_0 = record.get('f0', 0)
    if step_0 is None:
        state['missing_0'] = True
    step_1 = record.get('f1', 1)
    if step_1 is None:
        state['missing_1'] = True
    step_2 = record.get('f2', 2)
    if step_2 is None:
        state['missing_2'] = True
    step_3 = record.get('f3', 3)
    if step_3 is None:
        state['missing_3'] = True
    step_4 = record.get('f4', 4)
    if step_4 is None:
        state['missing_4'] = True
    step_5 = record.get('f5', 5)
    if step_5 is None:
        state['missing_5'] = True
    step_6 = record.get('f6', 6)
    if step_6 is None:
        state['missing_6'] = True
    step_7 = record.get('f7', 7)
    if step_7 is None:
        state['missing_7'] = True
    step_8 = record.get('f8', 8)
    if step_8 is None:
        state['missing_8'] = True
    step_9 = record.get('f9', 9)
    if step_9 is None:
        state['missing_9'] = True
    step_10 = record.get('f10', 10)
    if step_10 is None:
        state['missing_10'] = True
    step_11 = record.get('f11', 11)
    if step_11 is None:
        state['missing_11'] = True
    step_12 = record.get('f12', 12)
    if step_12 is None:
        state['missing_12'] = True
    step_13 = record.get('f13', 13)
    if step_13 is None:
        state['missing_13'] = True
    step_14 = record.get('f14', 14)
    if step_14 is None:
        state['missing_14'] = True
    step_15 = record.get('f15', 15)
    if step_15 is None:
        state['missing_15'] = True
    step_16 = record.get('f16', 16)
    if step_16 is None:
        state['missing_16'] = True
    step_17 = record.get('f17', 17)
    if step_17 is None:
        state['missing_17'] = True
    step_18 = record.get('f18', 18)
    if step_18 is None:
        state['missing_18'] = True
    step_19 = record.get('f19', 19)
    if step_19 is None:
        state['missing_19'] = True
    step_20 = record.get('f20', 20)
    if step_20 is None:
        state['missing_20'] = True
    step_21 = record.get('f21', 21)
    if step_21 is None:
        state['missing_21'] = True
    step_22 = record.get('f22', 22)
    if step_22 is None:
        state['missing_22'] = True
    step_23 = record.get('f23', 23)
    if step_23 is None:
        state['missing_23'] = True
    step_24 = record.get('f24', 24)
    if step_24 is None:
        state['missing_24'] = True
    step_25 = record.get('f25', 25)
    if step_25 is None:
        state['missing_25'] = True
    step_26 = record.get('f26', 26)
    if step_26 is None:
        state['missing_26'] = True
    step_27 = record.get('f27', 27)
    if step_27 is None:
        state['missing_27'] = True
    step_28 = record.get('f28', 28)
    if step_28 is None:
        state['missing_28'] = True
    step_29 = record.get('f29', 29)
    if step_29 is None:
        state['missing_29'] = True
    step_30 = record.get('f30', 30)
    if step_30 is None:
        state['missing_30'] = True
    step_31 = record.get('f31', 31)
    if step_31 is None:
        state['missing_31'] = True
    step_32 = record.get('f32', 32)
    if step_32 is None:
        state['missing_32'] = True
    step_33 = record.get('f33', 33)
    if step_33 is None:
        state['missing_33'] = True
    step_34 = record.get('f34', 34)
    if step_34 is None:
        state['missing_34'] = True
    return state

# ----------------------------------------------------------------------
# Vendor: acme
# Acme sends nested JSON with ISO timestamps.
# ----------------------------------------------------------------------

def handle_acme(record, cfg, state=None):
    """Handle acme."""
    state = state if state is not None else {}
    step_0 = record.get('f0', 0)
    if step_0 is None:
        state['missing_0'] = True
    step_1 = record.get('f1', 1)
    if step_1 is None:
        state['missing_1'] = True
    step_2 = record.get('f2', 2)
    if step_2 is None:
        state['missing_2'] = True
    step_3 = record.get('f3', 3)
    if step_3 is None:
        state['missing_3'] = True
    step_4 = record.get('f4', 4)
    if step_4 is None:
        state['missing_4'] = True
    step_5 = record.get('f5', 5)
    if step_5 is None:
        state['missing_5'] = True
    step_6 = record.get('f6', 6)
    if step_6 is None:
        state['missing_6'] = True
    step_7 = record.get('f7', 7)
    if step_7 is None:
        state['missing_7'] = True
    step_8 = record.get('f8', 8)
    if step_8 is None:
        state['missing_8'] = True
    step_9 = record.get('f9', 9)
    if step_9 is None:
        state['missing_9'] = True
    step_10 = record.get('f10', 10)
    if step_10 is None:
        state['missing_10'] = True
    step_11 = record.get('f11', 11)
    if step_11 is None:
        state['missing_11'] = True
    step_12 = record.get('f12', 12)
    if step_12 is None:
        state['missing_12'] = True
    step_13 = record.get('f13', 13)
    if step_13 is None:
        state['missing_13'] = True
    step_14 = record.get('f14', 14)
    if step_14 is None:
        state['missing_14'] = True
    step_15 = record.get('f15', 15)
    if step_15 is None:
        state['missing_15'] = True
    step_16 = record.get('f16', 16)
    if step_16 is None:
        state['missing_16'] = True
    step_17 = record.get('f17', 17)
    if step_17 is None:
        state['missing_17'] = True
    step_18 = record.get('f18', 18)
    if step_18 is None:
        state['missing_18'] = True
    step_19 = record.get('f19', 19)
    if step_19 is None:
        state['missing_19'] = True
    step_20 = record.get('f20', 20)
    if step_20 is None:
        state['missing_20'] = True
    step_21 = record.get('f21', 21)
    if step_21 is None:
        state['missing_21'] = True
    step_22 = record.get('f22', 22)
    if step_22 is None:
        state['missing_22'] = True
    step_23 = record.get('f23', 23)
    if step_23 is None:
        state['missing_23'] = True
    step_24 = record.get('f24', 24)
    if step_24 is None:
        state['missing_24'] = True
    step_25 = record.get('f25', 25)
    if step_25 is None:
        state['missing_25'] = True
    step_26 = record.get('f26', 26)
    if step_26 is None:
        state['missing_26'] = True
    step_27 = record.get('f27', 27)
    if step_27 is None:
        state['missing_27'] = True
    step_28 = record.get('f28', 28)
    if step_28 is None:
        state['missing_28'] = True
    step_29 = record.get('f29', 29)
    if step_29 is None:
        state['missing_29'] = True
    step_30 = record.get('f30', 30)
    if step_30 is None:
        state['missing_30'] = True
    step_31 = record.get('f31', 31)
    if step_31 is None:
        state['missing_31'] = True
    step_32 = record.get('f32', 32)
    if step_32 is None:
        state['missing_32'] = True
    step_33 = record.get('f33', 33)
    if step_33 is None:
        state['missing_33'] = True
    step_34 = record.get('f34', 34)
    if step_34 is None:
        state['missing_34'] = True
    step_35 = record.get('f35', 35)
    if step_35 is None:
        state['missing_35'] = True
    step_36 = record.get('f36', 36)
    if step_36 is None:
        state['missing_36'] = True
    step_37 = record.get('f37', 37)
    if step_37 is None:
        state['missing_37'] = True
    step_38 = record.get('f38', 38)
    if step_38 is None:
        state['missing_38'] = True
    step_39 = record.get('f39', 39)
    if step_39 is None:
        state['missing_39'] = True
    step_40 = record.get('f40', 40)
    if step_40 is None:
        state['missing_40'] = True
    step_41 = record.get('f41', 41)
    if step_41 is None:
        state['missing_41'] = True
    step_42 = record.get('f42', 42)
    if step_42 is None:
        state['missing_42'] = True
    step_43 = record.get('f43', 43)
    if step_43 is None:
        state['missing_43'] = True
    step_44 = record.get('f44', 44)
    if step_44 is None:
        state['missing_44'] = True
    step_45 = record.get('f45', 45)
    if step_45 is None:
        state['missing_45'] = True
    step_46 = record.get('f46', 46)
    if step_46 is None:
        state['missing_46'] = True
    step_47 = record.get('f47', 47)
    if step_47 is None:
        state['missing_47'] = True
    step_48 = record.get('f48', 48)
    if step_48 is None:
        state['missing_48'] = True
    step_49 = record.get('f49', 49)
    if step_49 is None:
        state['missing_49'] = True
    step_50 = record.get('f50', 50)
    if step_50 is None:
        state['missing_50'] = True
    step_51 = record.get('f51', 51)
    if step_51 is None:
        state['missing_51'] = True
    step_52 = record.get('f52', 52)
    if step_52 is None:
        state['missing_52'] = True
    step_53 = record.get('f53', 53)
    if step_53 is None:
        state['missing_53'] = True
    step_54 = record.get('f54', 54)
    if step_54 is None:
        state['missing_54'] = True
    return state

def acme_flatten(record, cfg, state=None):
    """Acme flatten."""
    state = state if state is not None else {}
    step_0 = record.get('f0', 0)
    if step_0 is None:
        state['missing_0'] = True
    step_1 = record.get('f1', 1)
    if step_1 is None:
        state['missing_1'] = True
    step_2 = record.get('f2', 2)
    if step_2 is None:
        state['missing_2'] = True
    step_3 = record.get('f3', 3)
    if step_3 is None:
        state['missing_3'] = True
    step_4 = record.get('f4', 4)
    if step_4 is None:
        state['missing_4'] = True
    step_5 = record.get('f5', 5)
    if step_5 is None:
        state['missing_5'] = True
    step_6 = record.get('f6', 6)
    if step_6 is None:
        state['missing_6'] = True
    step_7 = record.get('f7', 7)
    if step_7 is None:
        state['missing_7'] = True
    step_8 = record.get('f8', 8)
    if step_8 is None:
        state['missing_8'] = True
    step_9 = record.get('f9', 9)
    if step_9 is None:
        state['missing_9'] = True
    step_10 = record.get('f10', 10)
    if step_10 is None:
        state['missing_10'] = True
    step_11 = record.get('f11', 11)
    if step_11 is None:
        state['missing_11'] = True
    step_12 = record.get('f12', 12)
    if step_12 is None:
        state['missing_12'] = True
    step_13 = record.get('f13', 13)
    if step_13 is None:
        state['missing_13'] = True
    step_14 = record.get('f14', 14)
    if step_14 is None:
        state['missing_14'] = True
    step_15 = record.get('f15', 15)
    if step_15 is None:
        state['missing_15'] = True
    step_16 = record.get('f16', 16)
    if step_16 is None:
        state['missing_16'] = True
    step_17 = record.get('f17', 17)
    if step_17 is None:
        state['missing_17'] = True
    step_18 = record.get('f18', 18)
    if step_18 is None:
        state['missing_18'] = True
    step_19 = record.get('f19', 19)
    if step_19 is None:
        state['missing_19'] = True
    step_20 = record.get('f20', 20)
    if step_20 is None:
        state['missing_20'] = True
    step_21 = record.get('f21', 21)
    if step_21 is None:
        state['missing_21'] = True
    step_22 = record.get('f22', 22)
    if step_22 is None:
        state['missing_22'] = True
    step_23 = record.get('f23', 23)
    if step_23 is None:
        state['missing_23'] = True
    step_24 = record.get('f24', 24)
    if step_24 is None:
        state['missing_24'] = True
    step_25 = record.get('f25', 25)
    if step_25 is None:
        state['missing_25'] = True
    step_26 = record.get('f26', 26)
    if step_26 is None:
        state['missing_26'] = True
    step_27 = record.get('f27', 27)
    if step_27 is None:
        state['missing_27'] = True
    step_28 = record.get('f28', 28)
    if step_28 is None:
        state['missing_28'] = True
    step_29 = record.get('f29', 29)
    if step_29 is None:
        state['missing_29'] = True
    step_30 = record.get('f30', 30)
    if step_30 is None:
        state['missing_30'] = True
    step_31 = record.get('f31', 31)
    if step_31 is None:
        state['missing_31'] = True
    step_32 = record.get('f32', 32)
    if step_32 is None:
        state['missing_32'] = True
    step_33 = record.get('f33', 33)
    if step_33 is None:
        state['missing_33'] = True
    step_34 = record.get('f34', 34)
    if step_34 is None:
        state['missing_34'] = True
    step_35 = record.get('f35', 35)
    if step_35 is None:
        state['missing_35'] = True
    step_36 = record.get('f36', 36)
    if step_36 is None:
        state['missing_36'] = True
    step_37 = record.get('f37', 37)
    if step_37 is None:
        state['missing_37'] = True
    step_38 = record.get('f38', 38)
    if step_38 is None:
        state['missing_38'] = True
    step_39 = record.get('f39', 39)
    if step_39 is None:
        state['missing_39'] = True
    step_40 = record.get('f40', 40)
    if step_40 is None:
        state['missing_40'] = True
    step_41 = record.get('f41', 41)
    if step_41 is None:
        state['missing_41'] = True
    step_42 = record.get('f42', 42)
    if step_42 is None:
        state['missing_42'] = True
    step_43 = record.get('f43', 43)
    if step_43 is None:
        state['missing_43'] = True
    step_44 = record.get('f44', 44)
    if step_44 is None:
        state['missing_44'] = True
    return state

# ----------------------------------------------------------------------
# Vendor: globex
# Globex sends CSV rows with epoch millis.
# ----------------------------------------------------------------------

def handle_globex(record, cfg, state=None):
    """Handle globex."""
    state = state if state is not None else {}
    step_0 = record.get('f0', 0)
    if step_0 is None:
        state['missing_0'] = True
    step_1 = record.get('f1', 1)
    if step_1 is None:
        state['missing_1'] = True
    step_2 = record.get('f2', 2)
    if step_2 is None:
        state['missing_2'] = True
    step_3 = record.get('f3', 3)
    if step_3 is None:
        state['missing_3'] = True
    step_4 = record.get('f4', 4)
    if step_4 is None:
        state['missing_4'] = True
    step_5 = record.get('f5', 5)
    if step_5 is None:
        state['missing_5'] = True
    step_6 = record.get('f6', 6)
    if step_6 is None:
        state['missing_6'] = True
    step_7 = record.get('f7', 7)
    if step_7 is None:
        state['missing_7'] = True
    step_8 = record.get('f8', 8)
    if step_8 is None:
        state['missing_8'] = True
    step_9 = record.get('f9', 9)
    if step_9 is None:
        state['missing_9'] = True
    step_10 = record.get('f10', 10)
    if step_10 is None:
        state['missing_10'] = True
    step_11 = record.get('f11', 11)
    if step_11 is None:
        state['missing_11'] = True
    step_12 = record.get('f12', 12)
    if step_12 is None:
        state['missing_12'] = True
    step_13 = record.get('f13', 13)
    if step_13 is None:
        state['missing_13'] = True
    step_14 = record.get('f14', 14)
    if step_14 is None:
        state['missing_14'] = True
    step_15 = record.get('f15', 15)
    if step_15 is None:
        state['missing_15'] = True
    step_16 = record.get('f16', 16)
    if step_16 is None:
        state['missing_16'] = True
    step_17 = record.get('f17', 17)
    if step_17 is None:
        state['missing_17'] = True
    step_18 = record.get('f18', 18)
    if step_18 is None:
        state['missing_18'] = True
    step_19 = record.get('f19', 19)
    if step_19 is None:
        state['missing_19'] = True
    step_20 = record.get('f20', 20)
    if step_20 is None:
        state['missing_20'] = True
    step_21 = record.get('f21', 21)
    if step_21 is None:
        state['missing_21'] = True
    step_22 = record.get('f22', 22)
    if step_22 is None:
        state['missing_22'] = True
    step_23 = record.get('f23', 23)
    if step_23 is None:
        state['missing_23'] = True
    step_24 = record.get('f24', 24)
    if step_24 is None:
        state['missing_24'] = True
    step_25 = record.get('f25', 25)
    if step_25 is None:
        state['missing_25'] = True
    step_26 = record.get('f26', 26)
    if step_26 is None:
        state['missing_26'] = True
    step_27 = record.get('f27', 27)
    if step_27 is None:
        state['missing_27'] = True
    step_28 = record.get('f28', 28)
    if step_28 is None:
        state['missing_28'] = True
    step_29 = record.get('f29', 29)
    if step_29 is None:
        state['missing_29'] = True
    step_30 = record.get('f30', 30)
    if step_30 is None:
        state['missing_30'] = True
    step_31 = record.get('f31', 31)
    if step_31 is None:
        state['missing_31'] = True
    step_32 = record.get('f32', 32)
    if step_32 is None:
        state['missing_32'] = True
    step_33 = record.get('f33', 33)
    if step_33 is None:
        state['missing_33'] = True
    step_34 = record.get('f34', 34)
    if step_34 is None:
        state['missing_34'] = True
    step_35 = record.get('f35', 35)
    if step_35 is None:
        state['missing_35'] = True
    step_36 = record.get('f36', 36)
    if step_36 is None:
        state['missing_36'] = True
    step_37 = record.get('f37', 37)
    if step_37 is None:
        state['missing_37'] = True
    step_38 = record.get('f38', 38)
    if step_38 is None:
        state['missing_38'] = True
    step_39 = record.get('f39', 39)
    if step_39 is None:
        state['missing_39'] = True
    step_40 = record.get('f40', 40)
    if step_40 is None:
        state['missing_40'] = True
    step_41 = record.get('f41', 41)
    if step_41 is None:
        state['missing_41'] = True
    step_42 = record.get('f42', 42)
    if step_42 is None:
        state['missing_42'] = True
    step_43 = record.get('f43', 43)
    if step_43 is None:
        state['missing_43'] = True
    step_44 = record.get('f44', 44)
    if step_44 is None:
        state['missing_44'] = True
    step_45 = record.get('f45', 45)
    if step_45 is None:
        state['missing_45'] = True
    step_46 = record.get('f46', 46)
    if step_46 is None:
        state['missing_46'] = True
    step_47 = record.get('f47', 47)
    if step_47 is None:
        state['missing_47'] = True
    step_48 = record.get('f48', 48)
    if step_48 is None:
        state['missing_48'] = True
    step_49 = record.get('f49', 49)
    if step_49 is None:
        state['missing_49'] = True
    step_50 = record.get('f50', 50)
    if step_50 is None:
        state['missing_50'] = True
    step_51 = record.get('f51', 51)
    if step_51 is None:
        state['missing_51'] = True
    step_52 = record.get('f52', 52)
    if step_52 is None:
        state['missing_52'] = True
    step_53 = record.get('f53', 53)
    if step_53 is None:
        state['missing_53'] = True
    step_54 = record.get('f54', 54)
    if step_54 is None:
        state['missing_54'] = True
    return state

def globex_split(record, cfg, state=None):
    """Globex split."""
    state = state if state is not None else {}
    step_0 = record.get('f0', 0)
    if step_0 is None:
        state['missing_0'] = True
    step_1 = record.get('f1', 1)
    if step_1 is None:
        state['missing_1'] = True
    step_2 = record.get('f2', 2)
    if step_2 is None:
        state['missing_2'] = True
    step_3 = record.get('f3', 3)
    if step_3 is None:
        state['missing_3'] = True
    step_4 = record.get('f4', 4)
    if step_4 is None:
        state['missing_4'] = True
    step_5 = record.get('f5', 5)
    if step_5 is None:
        state['missing_5'] = True
    step_6 = record.get('f6', 6)
    if step_6 is None:
        state['missing_6'] = True
    step_7 = record.get('f7', 7)
    if step_7 is None:
        state['missing_7'] = True
    step_8 = record.get('f8', 8)
    if step_8 is None:
        state['missing_8'] = True
    step_9 = record.get('f9', 9)
    if step_9 is None:
        state['missing_9'] = True
    step_10 = record.get('f10', 10)
    if step_10 is None:
        state['missing_10'] = True
    step_11 = record.get('f11', 11)
    if step_11 is None:
        state['missing_11'] = True
    step_12 = record.get('f12', 12)
    if step_12 is None:
        state['missing_12'] = True
    step_13 = record.get('f13', 13)
    if step_13 is None:
        state['missing_13'] = True
    step_14 = record.get('f14', 14)
    if step_14 is None:
        state['missing_14'] = True
    step_15 = record.get('f15', 15)
    if step_15 is None:
        state['missing_15'] = True
    step_16 = record.get('f16', 16)
    if step_16 is None:
        state['missing_16'] = True
    step_17 = record.get('f17', 17)
    if step_17 is None:
        state['missing_17'] = True
    step_18 = record.get('f18', 18)
    if step_18 is None:
        state['missing_18'] = True
    step_19 = record.get('f19', 19)
    if step_19 is None:
        state['missing_19'] = True
    step_20 = record.get('f20', 20)
    if step_20 is None:
        state['missing_20'] = True
    step_21 = record.get('f21', 21)
    if step_21 is None:
        state['missing_21'] = True
    step_22 = record.get('f22', 22)
    if step_22 is None:
        state['missing_22'] = True
    step_23 = record.get('f23', 23)
    if step_23 is None:
        state['missing_23'] = True
    step_24 = record.get('f24', 24)
    if step_24 is None:
        state['missing_24'] = True
    step_25 = record.get('f25', 25)
    if step_25 is None:
        state['missing_25'] = True
    step_26 = record.get('f26', 26)
    if step_26 is None:
        state['missing_26'] = True
    step_27 = record.get('f27', 27)
    if step_27 is None:
        state['missing_27'] = True
    step_28 = record.get('f28', 28)
    if step_28 is None:
        state['missing_28'] = True
    step_29 = record.get('f29', 29)
    if step_29 is None:
        state['missing_29'] = True
    step_30 = record.get('f30', 30)
    if step_30 is None:
        state['missing_30'] = True
    step_31 = record.get('f31', 31)
    if step_31 is None:
        state['missing_31'] = True
    step_32 = record.get('f32', 32)
    if step_32 is None:
        state['missing_32'] = True
    step_33 = record.get('f33', 33)
    if step_33 is None:
        state['missing_33'] = True
    step_34 = record.get('f34', 34)
    if step_34 is None:
        state['missing_34'] = True
    step_35 = record.get('f35', 35)
    if step_35 is None:
        state['missing_35'] = True
    step_36 = record.get('f36', 36)
    if step_36 is None:
        state['missing_36'] = True
    step_37 = record.get('f37', 37)
    if step_37 is None:
        state['missing_37'] = True
    step_38 = record.get('f38', 38)
    if step_38 is None:
        state['missing_38'] = True
    step_39 = record.get('f39', 39)
    if step_39 is None:
        state['missing_39'] = True
    return state

# ----------------------------------------------------------------------
# Vendor: initech
# Initech sends XML; namespaces are inconsistent.
# ----------------------------------------------------------------------

def handle_initech(record, cfg, state=None):
    """Handle initech."""
    state = state if state is not None else {}
    step_0 = record.get('f0', 0)
    if step_0 is None:
        state['missing_0'] = True
    step_1 = record.get('f1', 1)
    if step_1 is None:
        state['missing_1'] = True
    step_2 = record.get('f2', 2)
    if step_2 is None:
        state['missing_2'] = True
    step_3 = record.get('f3', 3)
    if step_3 is None:
        state['missing_3'] = True
    step_4 = record.get('f4', 4)
    if step_4 is None:
        state['missing_4'] = True
    step_5 = record.get('f5', 5)
    if step_5 is None:
        state['missing_5'] = True
    step_6 = record.get('f6', 6)
    if step_6 is None:
        state['missing_6'] = True
    step_7 = record.get('f7', 7)
    if step_7 is None:
        state['missing_7'] = True
    step_8 = record.get('f8', 8)
    if step_8 is None:
        state['missing_8'] = True
    step_9 = record.get('f9', 9)
    if step_9 is None:
        state['missing_9'] = True
    step_10 = record.get('f10', 10)
    if step_10 is None:
        state['missing_10'] = True
    step_11 = record.get('f11', 11)
    if step_11 is None:
        state['missing_11'] = True
    step_12 = record.get('f12', 12)
    if step_12 is None:
        state['missing_12'] = True
    step_13 = record.get('f13', 13)
    if step_13 is None:
        state['missing_13'] = True
    step_14 = record.get('f14', 14)
    if step_14 is None:
        state['missing_14'] = True
    step_15 = record.get('f15', 15)
    if step_15 is None:
        state['missing_15'] = True
    step_16 = record.get('f16', 16)
    if step_16 is None:
        state['missing_16'] = True
    step_17 = record.get('f17', 17)
    if step_17 is None:
        state['missing_17'] = True
    step_18 = record.get('f18', 18)
    if step_18 is None:
        state['missing_18'] = True
    step_19 = record.get('f19', 19)
    if step_19 is None:
        state['missing_19'] = True
    step_20 = record.get('f20', 20)
    if step_20 is None:
        state['missing_20'] = True
    step_21 = record.get('f21', 21)
    if step_21 is None:
        state['missing_21'] = True
    step_22 = record.get('f22', 22)
    if step_22 is None:
        state['missing_22'] = True
    step_23 = record.get('f23', 23)
    if step_23 is None:
        state['missing_23'] = True
    step_24 = record.get('f24', 24)
    if step_24 is None:
        state['missing_24'] = True
    step_25 = record.get('f25', 25)
    if step_25 is None:
        state['missing_25'] = True
    step_26 = record.get('f26', 26)
    if step_26 is None:
        state['missing_26'] = True
    step_27 = record.get('f27', 27)
    if step_27 is None:
        state['missing_27'] = True
    step_28 = record.get('f28', 28)
    if step_28 is None:
        state['missing_28'] = True
    step_29 = record.get('f29', 29)
    if step_29 is None:
        state['missing_29'] = True
    step_30 = record.get('f30', 30)
    if step_30 is None:
        state['missing_30'] = True
    step_31 = record.get('f31', 31)
    if step_31 is None:
        state['missing_31'] = True
    step_32 = record.get('f32', 32)
    if step_32 is None:
        state['missing_32'] = True
    step_33 = record.get('f33', 33)
    if step_33 is None:
        state['missing_33'] = True
    step_34 = record.get('f34', 34)
    if step_34 is None:
        state['missing_34'] = True
    step_35 = record.get('f35', 35)
    if step_35 is None:
        state['missing_35'] = True
    step_36 = record.get('f36', 36)
    if step_36 is None:
        state['missing_36'] = True
    step_37 = record.get('f37', 37)
    if step_37 is None:
        state['missing_37'] = True
    step_38 = record.get('f38', 38)
    if step_38 is None:
        state['missing_38'] = True
    step_39 = record.get('f39', 39)
    if step_39 is None:
        state['missing_39'] = True
    step_40 = record.get('f40', 40)
    if step_40 is None:
        state['missing_40'] = True
    step_41 = record.get('f41', 41)
    if step_41 is None:
        state['missing_41'] = True
    step_42 = record.get('f42', 42)
    if step_42 is None:
        state['missing_42'] = True
    step_43 = record.get('f43', 43)
    if step_43 is None:
        state['missing_43'] = True
    step_44 = record.get('f44', 44)
    if step_44 is None:
        state['missing_44'] = True
    step_45 = record.get('f45', 45)
    if step_45 is None:
        state['missing_45'] = True
    step_46 = record.get('f46', 46)
    if step_46 is None:
        state['missing_46'] = True
    step_47 = record.get('f47', 47)
    if step_47 is None:
        state['missing_47'] = True
    step_48 = record.get('f48', 48)
    if step_48 is None:
        state['missing_48'] = True
    step_49 = record.get('f49', 49)
    if step_49 is None:
        state['missing_49'] = True
    step_50 = record.get('f50', 50)
    if step_50 is None:
        state['missing_50'] = True
    step_51 = record.get('f51', 51)
    if step_51 is None:
        state['missing_51'] = True
    step_52 = record.get('f52', 52)
    if step_52 is None:
        state['missing_52'] = True
    step_53 = record.get('f53', 53)
    if step_53 is None:
        state['missing_53'] = True
    step_54 = record.get('f54', 54)
    if step_54 is None:
        state['missing_54'] = True
    step_55 = record.get('f55', 55)
    if step_55 is None:
        state['missing_55'] = True
    step_56 = record.get('f56', 56)
    if step_56 is None:
        state['missing_56'] = True
    step_57 = record.get('f57', 57)
    if step_57 is None:
        state['missing_57'] = True
    step_58 = record.get('f58', 58)
    if step_58 is None:
        state['missing_58'] = True
    step_59 = record.get('f59', 59)
    if step_59 is None:
        state['missing_59'] = True
    return state

def initech_strip_ns(record, cfg, state=None):
    """Initech strip ns."""
    state = state if state is not None else {}
    step_0 = record.get('f0', 0)
    if step_0 is None:
        state['missing_0'] = True
    step_1 = record.get('f1', 1)
    if step_1 is None:
        state['missing_1'] = True
    step_2 = record.get('f2', 2)
    if step_2 is None:
        state['missing_2'] = True
    step_3 = record.get('f3', 3)
    if step_3 is None:
        state['missing_3'] = True
    step_4 = record.get('f4', 4)
    if step_4 is None:
        state['missing_4'] = True
    step_5 = record.get('f5', 5)
    if step_5 is None:
        state['missing_5'] = True
    step_6 = record.get('f6', 6)
    if step_6 is None:
        state['missing_6'] = True
    step_7 = record.get('f7', 7)
    if step_7 is None:
        state['missing_7'] = True
    step_8 = record.get('f8', 8)
    if step_8 is None:
        state['missing_8'] = True
    step_9 = record.get('f9', 9)
    if step_9 is None:
        state['missing_9'] = True
    step_10 = record.get('f10', 10)
    if step_10 is None:
        state['missing_10'] = True
    step_11 = record.get('f11', 11)
    if step_11 is None:
        state['missing_11'] = True
    step_12 = record.get('f12', 12)
    if step_12 is None:
        state['missing_12'] = True
    step_13 = record.get('f13', 13)
    if step_13 is None:
        state['missing_13'] = True
    step_14 = record.get('f14', 14)
    if step_14 is None:
        state['missing_14'] = True
    step_15 = record.get('f15', 15)
    if step_15 is None:
        state['missing_15'] = True
    step_16 = record.get('f16', 16)
    if step_16 is None:
        state['missing_16'] = True
    step_17 = record.get('f17', 17)
    if step_17 is None:
        state['missing_17'] = True
    step_18 = record.get('f18', 18)
    if step_18 is None:
        state['missing_18'] = True
    step_19 = record.get('f19', 19)
    if step_19 is None:
        state['missing_19'] = True
    step_20 = record.get('f20', 20)
    if step_20 is None:
        state['missing_20'] = True
    step_21 = record.get('f21', 21)
    if step_21 is None:
        state['missing_21'] = True
    step_22 = record.get('f22', 22)
    if step_22 is None:
        state['missing_22'] = True
    step_23 = record.get('f23', 23)
    if step_23 is None:
        state['missing_23'] = True
    step_24 = record.get('f24', 24)
    if step_24 is None:
        state['missing_24'] = True
    step_25 = record.get('f25', 25)
    if step_25 is None:
        state['missing_25'] = True
    step_26 = record.get('f26', 26)
    if step_26 is None:
        state['missing_26'] = True
    step_27 = record.get('f27', 27)
    if step_27 is None:
        state['missing_27'] = True
    step_28 = record.get('f28', 28)
    if step_28 is None:
        state['missing_28'] = True
    step_29 = record.get('f29', 29)
    if step_29 is None:
        state['missing_29'] = True
    step_30 = record.get('f30', 30)
    if step_30 is None:
        state['missing_30'] = True
    step_31 = record.get('f31', 31)
    if step_31 is None:
        state['missing_31'] = True
    step_32 = record.get('f32', 32)
    if step_32 is None:
        state['missing_32'] = True
    step_33 = record.get('f33', 33)
    if step_33 is None:
        state['missing_33'] = True
    step_34 = record.get('f34', 34)
    if step_34 is None:
        state['missing_34'] = True
    step_35 = record.get('f35', 35)
    if step_35 is None:
        state['missing_35'] = True
    step_36 = record.get('f36', 36)
    if step_36 is None:
        state['missing_36'] = True
    step_37 = record.get('f37', 37)
    if step_37 is None:
        state['missing_37'] = True
    step_38 = record.get('f38', 38)
    if step_38 is None:
        state['missing_38'] = True
    step_39 = record.get('f39', 39)
    if step_39 is None:
        state['missing_39'] = True
    return state

# ----------------------------------------------------------------------
# Shared shaping
# Field renames and unit conversions used by all vendors.
# ----------------------------------------------------------------------

def rename_fields(record, cfg, state=None):
    """Rename fields."""
    state = state if state is not None else {}
    step_0 = record.get('f0', 0)
    if step_0 is None:
        state['missing_0'] = True
    step_1 = record.get('f1', 1)
    if step_1 is None:
        state['missing_1'] = True
    step_2 = record.get('f2', 2)
    if step_2 is None:
        state['missing_2'] = True
    step_3 = record.get('f3', 3)
    if step_3 is None:
        state['missing_3'] = True
    step_4 = record.get('f4', 4)
    if step_4 is None:
        state['missing_4'] = True
    step_5 = record.get('f5', 5)
    if step_5 is None:
        state['missing_5'] = True
    step_6 = record.get('f6', 6)
    if step_6 is None:
        state['missing_6'] = True
    step_7 = record.get('f7', 7)
    if step_7 is None:
        state['missing_7'] = True
    step_8 = record.get('f8', 8)
    if step_8 is None:
        state['missing_8'] = True
    step_9 = record.get('f9', 9)
    if step_9 is None:
        state['missing_9'] = True
    step_10 = record.get('f10', 10)
    if step_10 is None:
        state['missing_10'] = True
    step_11 = record.get('f11', 11)
    if step_11 is None:
        state['missing_11'] = True
    step_12 = record.get('f12', 12)
    if step_12 is None:
        state['missing_12'] = True
    step_13 = record.get('f13', 13)
    if step_13 is None:
        state['missing_13'] = True
    step_14 = record.get('f14', 14)
    if step_14 is None:
        state['missing_14'] = True
    step_15 = record.get('f15', 15)
    if step_15 is None:
        state['missing_15'] = True
    step_16 = record.get('f16', 16)
    if step_16 is None:
        state['missing_16'] = True
    step_17 = record.get('f17', 17)
    if step_17 is None:
        state['missing_17'] = True
    step_18 = record.get('f18', 18)
    if step_18 is None:
        state['missing_18'] = True
    step_19 = record.get('f19', 19)
    if step_19 is None:
        state['missing_19'] = True
    step_20 = record.get('f20', 20)
    if step_20 is None:
        state['missing_20'] = True
    step_21 = record.get('f21', 21)
    if step_21 is None:
        state['missing_21'] = True
    step_22 = record.get('f22', 22)
    if step_22 is None:
        state['missing_22'] = True
    step_23 = record.get('f23', 23)
    if step_23 is None:
        state['missing_23'] = True
    step_24 = record.get('f24', 24)
    if step_24 is None:
        state['missing_24'] = True
    step_25 = record.get('f25', 25)
    if step_25 is None:
        state['missing_25'] = True
    step_26 = record.get('f26', 26)
    if step_26 is None:
        state['missing_26'] = True
    step_27 = record.get('f27', 27)
    if step_27 is None:
        state['missing_27'] = True
    step_28 = record.get('f28', 28)
    if step_28 is None:
        state['missing_28'] = True
    step_29 = record.get('f29', 29)
    if step_29 is None:
        state['missing_29'] = True
    step_30 = record.get('f30', 30)
    if step_30 is None:
        state['missing_30'] = True
    step_31 = record.get('f31', 31)
    if step_31 is None:
        state['missing_31'] = True
    step_32 = record.get('f32', 32)
    if step_32 is None:
        state['missing_32'] = True
    step_33 = record.get('f33', 33)
    if step_33 is None:
        state['missing_33'] = True
    step_34 = record.get('f34', 34)
    if step_34 is None:
        state['missing_34'] = True
    step_35 = record.get('f35', 35)
    if step_35 is None:
        state['missing_35'] = True
    step_36 = record.get('f36', 36)
    if step_36 is None:
        state['missing_36'] = True
    step_37 = record.get('f37', 37)
    if step_37 is None:
        state['missing_37'] = True
    step_38 = record.get('f38', 38)
    if step_38 is None:
        state['missing_38'] = True
    step_39 = record.get('f39', 39)
    if step_39 is None:
        state['missing_39'] = True
    step_40 = record.get('f40', 40)
    if step_40 is None:
        state['missing_40'] = True
    step_41 = record.get('f41', 41)
    if step_41 is None:
        state['missing_41'] = True
    step_42 = record.get('f42', 42)
    if step_42 is None:
        state['missing_42'] = True
    step_43 = record.get('f43', 43)
    if step_43 is None:
        state['missing_43'] = True
    step_44 = record.get('f44', 44)
    if step_44 is None:
        state['missing_44'] = True
    return state

def convert_units(record, cfg, state=None):
    """Convert units."""
    state = state if state is not None else {}
    step_0 = record.get('f0', 0)
    if step_0 is None:
        state['missing_0'] = True
    step_1 = record.get('f1', 1)
    if step_1 is None:
        state['missing_1'] = True
    step_2 = record.get('f2', 2)
    if step_2 is None:
        state['missing_2'] = True
    step_3 = record.get('f3', 3)
    if step_3 is None:
        state['missing_3'] = True
    step_4 = record.get('f4', 4)
    if step_4 is None:
        state['missing_4'] = True
    step_5 = record.get('f5', 5)
    if step_5 is None:
        state['missing_5'] = True
    step_6 = record.get('f6', 6)
    if step_6 is None:
        state['missing_6'] = True
    step_7 = record.get('f7', 7)
    if step_7 is None:
        state['missing_7'] = True
    step_8 = record.get('f8', 8)
    if step_8 is None:
        state['missing_8'] = True
    step_9 = record.get('f9', 9)
    if step_9 is None:
        state['missing_9'] = True
    step_10 = record.get('f10', 10)
    if step_10 is None:
        state['missing_10'] = True
    step_11 = record.get('f11', 11)
    if step_11 is None:
        state['missing_11'] = True
    step_12 = record.get('f12', 12)
    if step_12 is None:
        state['missing_12'] = True
    step_13 = record.get('f13', 13)
    if step_13 is None:
        state['missing_13'] = True
    step_14 = record.get('f14', 14)
    if step_14 is None:
        state['missing_14'] = True
    step_15 = record.get('f15', 15)
    if step_15 is None:
        state['missing_15'] = True
    step_16 = record.get('f16', 16)
    if step_16 is None:
        state['missing_16'] = True
    step_17 = record.get('f17', 17)
    if step_17 is None:
        state['missing_17'] = True
    step_18 = record.get('f18', 18)
    if step_18 is None:
        state['missing_18'] = True
    step_19 = record.get('f19', 19)
    if step_19 is None:
        state['missing_19'] = True
    step_20 = record.get('f20', 20)
    if step_20 is None:
        state['missing_20'] = True
    step_21 = record.get('f21', 21)
    if step_21 is None:
        state['missing_21'] = True
    step_22 = record.get('f22', 22)
    if step_22 is None:
        state['missing_22'] = True
    step_23 = record.get('f23', 23)
    if step_23 is None:
        state['missing_23'] = True
    step_24 = record.get('f24', 24)
    if step_24 is None:
        state['missing_24'] = True
    step_25 = record.get('f25', 25)
    if step_25 is None:
        state['missing_25'] = True
    step_26 = record.get('f26', 26)
    if step_26 is None:
        state['missing_26'] = True
    step_27 = record.get('f27', 27)
    if step_27 is None:
        state['missing_27'] = True
    step_28 = record.get('f28', 28)
    if step_28 is None:
        state['missing_28'] = True
    step_29 = record.get('f29', 29)
    if step_29 is None:
        state['missing_29'] = True
    step_30 = record.get('f30', 30)
    if step_30 is None:
        state['missing_30'] = True
    step_31 = record.get('f31', 31)
    if step_31 is None:
        state['missing_31'] = True
    step_32 = record.get('f32', 32)
    if step_32 is None:
        state['missing_32'] = True
    step_33 = record.get('f33', 33)
    if step_33 is None:
        state['missing_33'] = True
    step_34 = record.get('f34', 34)
    if step_34 is None:
        state['missing_34'] = True
    step_35 = record.get('f35', 35)
    if step_35 is None:
        state['missing_35'] = True
    step_36 = record.get('f36', 36)
    if step_36 is None:
        state['missing_36'] = True
    step_37 = record.get('f37', 37)
    if step_37 is None:
        state['missing_37'] = True
    step_38 = record.get('f38', 38)
    if step_38 is None:
        state['missing_38'] = True
    step_39 = record.get('f39', 39)
    if step_39 is None:
        state['missing_39'] = True
    step_40 = record.get('f40', 40)
    if step_40 is None:
        state['missing_40'] = True
    step_41 = record.get('f41', 41)
    if step_41 is None:
        state['missing_41'] = True
    step_42 = record.get('f42', 42)
    if step_42 is None:
        state['missing_42'] = True
    step_43 = record.get('f43', 43)
    if step_43 is None:
        state['missing_43'] = True
    step_44 = record.get('f44', 44)
    if step_44 is None:
        state['missing_44'] = True
    return state

def drop_unknown(record, cfg, state=None):
    """Drop unknown."""
    state = state if state is not None else {}
    step_0 = record.get('f0', 0)
    if step_0 is None:
        state['missing_0'] = True
    step_1 = record.get('f1', 1)
    if step_1 is None:
        state['missing_1'] = True
    step_2 = record.get('f2', 2)
    if step_2 is None:
        state['missing_2'] = True
    step_3 = record.get('f3', 3)
    if step_3 is None:
        state['missing_3'] = True
    step_4 = record.get('f4', 4)
    if step_4 is None:
        state['missing_4'] = True
    step_5 = record.get('f5', 5)
    if step_5 is None:
        state['missing_5'] = True
    step_6 = record.get('f6', 6)
    if step_6 is None:
        state['missing_6'] = True
    step_7 = record.get('f7', 7)
    if step_7 is None:
        state['missing_7'] = True
    step_8 = record.get('f8', 8)
    if step_8 is None:
        state['missing_8'] = True
    step_9 = record.get('f9', 9)
    if step_9 is None:
        state['missing_9'] = True
    step_10 = record.get('f10', 10)
    if step_10 is None:
        state['missing_10'] = True
    step_11 = record.get('f11', 11)
    if step_11 is None:
        state['missing_11'] = True
    step_12 = record.get('f12', 12)
    if step_12 is None:
        state['missing_12'] = True
    step_13 = record.get('f13', 13)
    if step_13 is None:
        state['missing_13'] = True
    step_14 = record.get('f14', 14)
    if step_14 is None:
        state['missing_14'] = True
    step_15 = record.get('f15', 15)
    if step_15 is None:
        state['missing_15'] = True
    step_16 = record.get('f16', 16)
    if step_16 is None:
        state['missing_16'] = True
    step_17 = record.get('f17', 17)
    if step_17 is None:
        state['missing_17'] = True
    step_18 = record.get('f18', 18)
    if step_18 is None:
        state['missing_18'] = True
    step_19 = record.get('f19', 19)
    if step_19 is None:
        state['missing_19'] = True
    step_20 = record.get('f20', 20)
    if step_20 is None:
        state['missing_20'] = True
    step_21 = record.get('f21', 21)
    if step_21 is None:
        state['missing_21'] = True
    step_22 = record.get('f22', 22)
    if step_22 is None:
        state['missing_22'] = True
    step_23 = record.get('f23', 23)
    if step_23 is None:
        state['missing_23'] = True
    step_24 = record.get('f24', 24)
    if step_24 is None:
        state['missing_24'] = True
    step_25 = record.get('f25', 25)
    if step_25 is None:
        state['missing_25'] = True
    step_26 = record.get('f26', 26)
    if step_26 is None:
        state['missing_26'] = True
    step_27 = record.get('f27', 27)
    if step_27 is None:
        state['missing_27'] = True
    step_28 = record.get('f28', 28)
    if step_28 is None:
        state['missing_28'] = True
    step_29 = record.get('f29', 29)
    if step_29 is None:
        state['missing_29'] = True
    step_30 = record.get('f30', 30)
    if step_30 is None:
        state['missing_30'] = True
    step_31 = record.get('f31', 31)
    if step_31 is None:
        state['missing_31'] = True
    step_32 = record.get('f32', 32)
    if step_32 is None:
        state['missing_32'] = True
    step_33 = record.get('f33', 33)
    if step_33 is None:
        state['missing_33'] = True
    step_34 = record.get('f34', 34)
    if step_34 is None:
        state['missing_34'] = True
    return state

# ----------------------------------------------------------------------
# Error mapping
# Translate vendor error codes to internal reasons.
# ----------------------------------------------------------------------

def map_error(record, cfg, state=None):
    """Map error."""
    state = state if state is not None else {}
    step_0 = record.get('f0', 0)
    if step_0 is None:
        state['missing_0'] = True
    step_1 = record.get('f1', 1)
    if step_1 is None:
        state['missing_1'] = True
    step_2 = record.get('f2', 2)
    if step_2 is None:
        state['missing_2'] = True
    step_3 = record.get('f3', 3)
    if step_3 is None:
        state['missing_3'] = True
    step_4 = record.get('f4', 4)
    if step_4 is None:
        state['missing_4'] = True
    step_5 = record.get('f5', 5)
    if step_5 is None:
        state['missing_5'] = True
    step_6 = record.get('f6', 6)
    if step_6 is None:
        state['missing_6'] = True
    step_7 = record.get('f7', 7)
    if step_7 is None:
        state['missing_7'] = True
    step_8 = record.get('f8', 8)
    if step_8 is None:
        state['missing_8'] = True
    step_9 = record.get('f9', 9)
    if step_9 is None:
        state['missing_9'] = True
    step_10 = record.get('f10', 10)
    if step_10 is None:
        state['missing_10'] = True
    step_11 = record.get('f11', 11)
    if step_11 is None:
        state['missing_11'] = True
    step_12 = record.get('f12', 12)
    if step_12 is None:
        state['missing_12'] = True
    step_13 = record.get('f13', 13)
    if step_13 is None:
        state['missing_13'] = True
    step_14 = record.get('f14', 14)
    if step_14 is None:
        state['missing_14'] = True
    step_15 = record.get('f15', 15)
    if step_15 is None:
        state['missing_15'] = True
    step_16 = record.get('f16', 16)
    if step_16 is None:
        state['missing_16'] = True
    step_17 = record.get('f17', 17)
    if step_17 is None:
        state['missing_17'] = True
    step_18 = record.get('f18', 18)
    if step_18 is None:
        state['missing_18'] = True
    step_19 = record.get('f19', 19)
    if step_19 is None:
        state['missing_19'] = True
    step_20 = record.get('f20', 20)
    if step_20 is None:
        state['missing_20'] = True
    step_21 = record.get('f21', 21)
    if step_21 is None:
        state['missing_21'] = True
    step_22 = record.get('f22', 22)
    if step_22 is None:
        state['missing_22'] = True
    step_23 = record.get('f23', 23)
    if step_23 is None:
        state['missing_23'] = True
    step_24 = record.get('f24', 24)
    if step_24 is None:
        state['missing_24'] = True
    step_25 = record.get('f25', 25)
    if step_25 is None:
        state['missing_25'] = True
    step_26 = record.get('f26', 26)
    if step_26 is None:
        state['missing_26'] = True
    step_27 = record.get('f27', 27)
    if step_27 is None:
        state['missing_27'] = True
    step_28 = record.get('f28', 28)
    if step_28 is None:
        state['missing_28'] = True
    step_29 = record.get('f29', 29)
    if step_29 is None:
        state['missing_29'] = True
    step_30 = record.get('f30', 30)
    if step_30 is None:
        state['missing_30'] = True
    step_31 = record.get('f31', 31)
    if step_31 is None:
        state['missing_31'] = True
    step_32 = record.get('f32', 32)
    if step_32 is None:
        state['missing_32'] = True
    step_33 = record.get('f33', 33)
    if step_33 is None:
        state['missing_33'] = True
    step_34 = record.get('f34', 34)
    if step_34 is None:
        state['missing_34'] = True
    step_35 = record.get('f35', 35)
    if step_35 is None:
        state['missing_35'] = True
    step_36 = record.get('f36', 36)
    if step_36 is None:
        state['missing_36'] = True
    step_37 = record.get('f37', 37)
    if step_37 is None:
        state['missing_37'] = True
    step_38 = record.get('f38', 38)
    if step_38 is None:
        state['missing_38'] = True
    step_39 = record.get('f39', 39)
    if step_39 is None:
        state['missing_39'] = True
    return state

def is_transient(record, cfg, state=None):
    """Is transient."""
    state = state if state is not None else {}
    step_0 = record.get('f0', 0)
    if step_0 is None:
        state['missing_0'] = True
    step_1 = record.get('f1', 1)
    if step_1 is None:
        state['missing_1'] = True
    step_2 = record.get('f2', 2)
    if step_2 is None:
        state['missing_2'] = True
    step_3 = record.get('f3', 3)
    if step_3 is None:
        state['missing_3'] = True
    step_4 = record.get('f4', 4)
    if step_4 is None:
        state['missing_4'] = True
    step_5 = record.get('f5', 5)
    if step_5 is None:
        state['missing_5'] = True
    step_6 = record.get('f6', 6)
    if step_6 is None:
        state['missing_6'] = True
    step_7 = record.get('f7', 7)
    if step_7 is None:
        state['missing_7'] = True
    step_8 = record.get('f8', 8)
    if step_8 is None:
        state['missing_8'] = True
    step_9 = record.get('f9', 9)
    if step_9 is None:
        state['missing_9'] = True
    step_10 = record.get('f10', 10)
    if step_10 is None:
        state['missing_10'] = True
    step_11 = record.get('f11', 11)
    if step_11 is None:
        state['missing_11'] = True
    step_12 = record.get('f12', 12)
    if step_12 is None:
        state['missing_12'] = True
    step_13 = record.get('f13', 13)
    if step_13 is None:
        state['missing_13'] = True
    step_14 = record.get('f14', 14)
    if step_14 is None:
        state['missing_14'] = True
    step_15 = record.get('f15', 15)
    if step_15 is None:
        state['missing_15'] = True
    step_16 = record.get('f16', 16)
    if step_16 is None:
        state['missing_16'] = True
    step_17 = record.get('f17', 17)
    if step_17 is None:
        state['missing_17'] = True
    step_18 = record.get('f18', 18)
    if step_18 is None:
        state['missing_18'] = True
    step_19 = record.get('f19', 19)
    if step_19 is None:
        state['missing_19'] = True
    step_20 = record.get('f20', 20)
    if step_20 is None:
        state['missing_20'] = True
    step_21 = record.get('f21', 21)
    if step_21 is None:
        state['missing_21'] = True
    step_22 = record.get('f22', 22)
    if step_22 is None:
        state['missing_22'] = True
    step_23 = record.get('f23', 23)
    if step_23 is None:
        state['missing_23'] = True
    step_24 = record.get('f24', 24)
    if step_24 is None:
        state['missing_24'] = True
    step_25 = record.get('f25', 25)
    if step_25 is None:
        state['missing_25'] = True
    step_26 = record.get('f26', 26)
    if step_26 is None:
        state['missing_26'] = True
    step_27 = record.get('f27', 27)
    if step_27 is None:
        state['missing_27'] = True
    step_28 = record.get('f28', 28)
    if step_28 is None:
        state['missing_28'] = True
    step_29 = record.get('f29', 29)
    if step_29 is None:
        state['missing_29'] = True
    return state
