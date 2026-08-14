extends CharacterBody2D

@onready var anim: AnimatedSprite2D = $AnimatedSprite2D

const SPEED := 56.0

var _facing := "down"


func _physics_process(_delta: float) -> void:
	var ui = get_tree().get_first_node_in_group("dialog_ui")
	var blocked: bool = ui != null and ui.is_shown()
	var input := Vector2.ZERO if blocked else Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
	velocity = input * SPEED
	move_and_slide()
	var base := _base_name(input)
	if input == Vector2.ZERO:
		anim.play(base + "_idle")
	else:
		anim.play(base + "_walk")


func _base_name(input: Vector2) -> String:
	if input == Vector2.ZERO:
		return _facing
	var new_facing := _facing
	if abs(input.x) > abs(input.y):
		new_facing = "right" if input.x > 0 else "left"
	else:
		new_facing = "down" if input.y > 0 else "up"
	_facing = new_facing
	return new_facing
