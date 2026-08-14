extends Interactable

var _interacted := false


func _unhandled_input(event: InputEvent) -> void:
	if not player_in or not event.is_action_pressed("ui_accept") or GameState.game_over or _interacted:
		return
	var ui = get_tree().get_first_node_in_group("dialog_ui")
	if ui == null or ui.is_shown():
		return
	ui.show_choices("YOOO whats good.", ["where am i?", "ayy im chilling. hbu?"], _on_choice)
	get_viewport().set_input_as_handled()


func _on_choice(index: int) -> void:
	_interacted = true
	var ui = get_tree().get_first_node_in_group("dialog_ui")
	if ui == null:
		return
	if index == 0:
		ui.show_message("my dream. duh.")
	else:
		GameState.resolve_good_ending()
		ui.show_message("alright.")
