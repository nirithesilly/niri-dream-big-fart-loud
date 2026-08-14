extends Interactable

var _consumed := false


func _unhandled_input(event: InputEvent) -> void:
	if not player_in or not event.is_action_pressed("ui_accept") or GameState.game_over or _consumed:
		return
	var ui = get_tree().get_first_node_in_group("dialog_ui")
	if ui == null or ui.is_shown():
		return
	ui.show_choices("a candy.", ["eat.", "take.", "leave."], _on_choice)
	get_viewport().set_input_as_handled()


func _on_choice(index: int) -> void:
	match index:
		0:
			_consumed = true
			GameState.has_candy = false
			Engine.time_scale = 2.0
			visible = false
		1:
			_consumed = true
			GameState.has_candy = true
			visible = false
		2:
			pass
