

def test_action_init_without_injection(action):
    assert 'Mouse object' in str(action.mouse)
    assert 'Keyboard object' in str(action.keyboard)
    assert 'Hotkeys object' in str(action.hotkeys)


def test_action_init_with_injection():
    from control.controller import Action
    action = Action(mouse=object, keyboard=object, hotkeys=object)
    assert action.mouse is object
    assert action.keyboard is object
    assert action.hotkeys is object
