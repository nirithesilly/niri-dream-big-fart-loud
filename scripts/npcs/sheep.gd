extends Interactable

const SCATTER_SPEED := 180.0
const SCATTER_LIFETIME := 6.0

var _scattering := false
var _dir := Vector2.RIGHT
var _t := 0.0
var _origin := Vector2.ZERO


func _ready() -> void:
	super()
	_origin = global_position


func _unhandled_input(event: InputEvent) -> void:
	if not player_in or not event.is_action_pressed("ui_accept") or GameState.game_over:
		return
	var ui = get_tree().get_first_node_in_group("dialog_ui")
	if ui == null or ui.is_shown():
		return
	if GameState.good_ending and GameState.has_candy:
		ui.show_choices("...", ["give the candy", "leave"], _on_choice)
	else:
		ui.show_message(text)
	get_viewport().set_input_as_handled()


func _on_choice(index: int) -> void:
	if index == 0:
		GameState.has_candy = false
		var ui = get_tree().get_first_node_in_group("dialog_ui")
		if ui:
			ui.show_message("you are worthless.")


func scatter() -> void:
	_scattering = true
	player_in = false
	_dir = global_position - _origin
	if _dir.length() < 1.0:
		_dir = Vector2.RIGHT
	_dir = _dir.normalized()


func _physics_process(delta: float) -> void:
	if not _scattering:
		return
	_t += delta
	global_position += _dir * SCATTER_SPEED * delta
	if _t > SCATTER_LIFETIME:
		queue_free()
