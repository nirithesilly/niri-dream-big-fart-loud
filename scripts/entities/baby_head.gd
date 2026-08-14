extends CharacterBody2D

const CHASE_SPEED := 52.0
const AGGRO_DIST := 110.0
const CATCH_DIST := 8.0
const GRAF_REACH := 60.0

var player: CharacterBody2D = null
var wolf: Node2D = null
var _elapsed := 0.0

@onready var sprite: Sprite2D = $Sprite2D


func _ready() -> void:
	player = get_tree().get_first_node_in_group("player")
	wolf = get_tree().get_first_node_in_group("wolf")


func _physics_process(delta: float) -> void:
	if GameState.game_over or GameState.head_resolved:
		return
	_elapsed += delta
	sprite.position.y = sin(_elapsed * 2.0) * 2.0
	if player == null:
		return
	if wolf != null and global_position.distance_to(wolf.global_position) < GRAF_REACH:
		GameState.resolve_head()
		return
	var to_player: Vector2 = player.global_position - global_position
	var dist := to_player.length()
	if dist < CATCH_DIST:
		GameState.trigger_game_over()
		return
	if dist < AGGRO_DIST:
		velocity = to_player / dist * CHASE_SPEED
	else:
		velocity = Vector2.ZERO
	move_and_slide()
