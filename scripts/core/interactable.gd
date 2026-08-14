class_name Interactable
extends Area2D

@export_multiline var text := ""

var player_in := false


func _ready() -> void:
	body_entered.connect(_on_body_entered)
	body_exited.connect(_on_body_exited)


func _on_body_entered(body: Node) -> void:
	if body.is_in_group("player"):
		player_in = true


func _on_body_exited(body: Node) -> void:
	if body.is_in_group("player"):
		player_in = false


func _unhandled_input(event: InputEvent) -> void:
	if not player_in or not event.is_action_pressed("ui_accept"):
		return
	var ui = get_tree().get_first_node_in_group("dialog_ui")
	if ui == null or ui.is_shown():
		return
	ui.show_message(text)
	get_viewport().set_input_as_handled()
