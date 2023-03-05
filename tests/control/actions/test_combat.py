

def test_action_init_without_injection(combat):
    assert 'Combat object' in str(combat)
    assert 'Mouse object' in str(combat.mouse)
    assert 'Keyboard object' in str(combat.keyboard)
    assert 'Hotkeys object' in str(combat.hotkeys)
