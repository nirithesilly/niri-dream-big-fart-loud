
extends Interactable

const FLY_SPEED := 56.0
const FLEE_SPEED := 300.0

var head: Node2D = null
var triggered := false
var landed := false
var eyes_closed := false
var blame := false
var fled := false

@onready var sprite: Sprite2D = $Sprite2D


func _ready() -> void:
	super()
	head = get_tree().get_first_node_in_group("baby_head")


func close_eyes() -> void:
	eyes_closed = true
	$Sprite2D.visible = false
	$ClosedSprite.visible = true


func mark_blame() -> void:
	blame = true


func start_flee() -> void:
	fled = true


func _unhandled_input(event: InputEvent) -> void:
	if not player_in or not event.is_action_pressed("ui_accept") or GameState.game_over or fled:
		return
	var ui = get_tree().get_first_node_in_group("dialog_ui")
	if ui == null or ui.is_shown():
		return
	if blame:
		ui.show_sequence(["its your fault"], start_flee)
	elif eyes_closed:
		ui.show_sequence(["it is not supposed to...", "..."], start_flee)
	elif not triggered:
		triggered = true
	else:
		return
	get_viewport().set_input_as_handled()


func _physics_process(delta: float) -> void:
	if GameState.game_over:
		return
	if fled:
		global_position.x += FLEE_SPEED * delta
		if global_position.x > 3400.0:
			visible = false
		return
	if eyes_closed:
		_bob()
		return
	if triggered and not landed:
		if head == null:
			landed = true
			return
		var target := head.global_position + Vector2(16, -8)
		var to_target := target - global_position
		var dist := to_target.length()
		if dist < FLY_SPEED * delta:
			global_position = target
			landed = true
		else:
			global_position += to_target / dist * FLY_SPEED * delta
	_bob()


func _bob() -> void:
	sprite.position.x = sin(Time.get_ticks_msec() * 0.004) * 1.5
	sprite.position.y = sin(Time.get_ticks_msec() * 0.006) * 1.5
