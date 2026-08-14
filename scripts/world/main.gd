extends Node2D

const MAP_W := 200
const MAP_H := 150
const CLEAR_RADIUS := 5.0
const TREE_STEP := 3
const TREE_DENSITY := 0.35
const GRAF_CLEAR_RADIUS := 90.0

const GRAF_POS := Vector2(1400, 1208)
const HEAD_POS := Vector2(3060, 1240)
const OWL_TREE_POS := Vector2(1712, 1184)
const CANDY_POS := Vector2(1760, 1040)
const SELF_POS := Vector2(120, 2296)
const SELF_CLEAR_RADIUS := 64.0
const SELF_BORDER_CLEAR := 75.0

var tree_scene: PackedScene = preload("res://scenes/world/Tree.tscn")
var graf_scene: PackedScene = preload("res://scenes/npcs/Graf.tscn")
var sheep_scene: PackedScene = preload("res://scenes/npcs/Sheep.tscn")
var baby_head_scene: PackedScene = preload("res://scenes/entities/BabyHead.tscn")
var owl_scene: PackedScene = preload("res://scenes/npcs/Owl.tscn")
var candy_scene: PackedScene = preload("res://scenes/items/Candy.tscn")
var self_scene: PackedScene = preload("res://scenes/npcs/Self.tscn")
var dialog_scene: PackedScene = preload("res://scenes/ui/DialogUI.tscn")

@onready var ground: TileMapLayer = $Ground
@onready var ysort: Node2D = $YSort

var rng := RandomNumberGenerator.new()


func _ready() -> void:
	rng.seed = 42
	add_child(dialog_scene.instantiate())
	_fill_ground()
	_spawn_border_trees()
	_spawn_trees()
	_build_walls()
	_spawn_graf_and_sheep()
	_spawn_baby_head()
	_spawn_owl()
	_spawn_candy()
	_spawn_self()


func _fill_ground() -> void:
	for y in range(MAP_H):
		for x in range(MAP_W):
			if _in_clear_zone(x, y) and rng.randf() < 0.7:
				continue
			var variant := rng.randi_range(0, 7)
			ground.set_cell(Vector2i(x, y), 0, Vector2i(variant % 4, variant / 4))

func _spawn_border_trees() -> void:
	for x in range(MAP_W):
		for y in range(MAP_H):
			if _is_border(x, y):
				var pos := Vector2(x * 16 + 8, y * 16 + 8)
				if pos.distance_to(SELF_POS) < SELF_BORDER_CLEAR:
					continue
				_add_tree(pos, Vector2.ZERO)

func _spawn_trees() -> void:
	for x in range(0, MAP_W, TREE_STEP):
		for y in range(0, MAP_H, TREE_STEP):
			if _is_border(x, y) or _in_clear_zone(x, y) or _in_graf_clearing(x, y) or _in_head_clearing(x, y) or _in_owl_tree_clearing(x, y) or _in_candy_clearing(x, y) or _in_self_clearing(x, y) or rng.randf() > TREE_DENSITY:
				continue
			_add_tree(Vector2(x * 16 + 8, y * 16 + 8), Vector2(rng.randf_range(-4, 4), rng.randf_range(-4, 4)))

func _is_border(x: int, y: int) -> bool:
	return x < 2 or x >= MAP_W - 2 or y < 2 or y >= MAP_H - 2

func _add_tree(pos: Vector2, jitter: Vector2) -> void:
	var tree: StaticBody2D = tree_scene.instantiate()
	tree.position = pos + jitter
	ysort.add_child(tree)

func _build_walls() -> void:
	var size := Vector2(MAP_W * 16.0, MAP_H * 16.0)
	_add_wall(Vector2(size.x / 2.0, -8.0), Vector2(size.x, 16.0))
	_add_wall(Vector2(size.x / 2.0, size.y + 8.0), Vector2(size.x, 16.0))
	_add_wall(Vector2(-8.0, size.y / 2.0), Vector2(16.0, size.y))
	_add_wall(Vector2(size.x + 8.0, size.y / 2.0), Vector2(16.0, size.y))

func _add_wall(pos: Vector2, sz: Vector2) -> void:
	var wall := StaticBody2D.new()
	var shape := CollisionShape2D.new()
	var rect := RectangleShape2D.new()
	rect.size = sz
	shape.shape = rect
	wall.add_child(shape)
	wall.position = pos
	add_child(wall)


func _spawn_graf_and_sheep() -> void:
	var graf := graf_scene.instantiate()
	graf.position = GRAF_POS
	ysort.add_child(graf)
	var sheep_offsets := [Vector2(-26, -10), Vector2(-40, 12), Vector2(-54, -4)]
	for off in sheep_offsets:
		var sheep := sheep_scene.instantiate()
		sheep.position = GRAF_POS + off
		ysort.add_child(sheep)

func _spawn_baby_head() -> void:
	var head := baby_head_scene.instantiate()
	head.position = HEAD_POS
	ysort.add_child(head)

func _spawn_owl() -> void:
	var tree := tree_scene.instantiate()
	tree.position = OWL_TREE_POS
	ysort.add_child(tree)
	var owl := owl_scene.instantiate()
	owl.position = Vector2(0, -44)
	tree.add_child(owl)

func _spawn_candy() -> void:
	var candy := candy_scene.instantiate()
	candy.position = CANDY_POS
	ysort.add_child(candy)

func _spawn_self() -> void:
	var self_npc := self_scene.instantiate()
	self_npc.position = SELF_POS
	ysort.add_child(self_npc)


func _in_graf_clearing(x: int, y: int) -> bool:
	var p := Vector2(x * 16.0 + 8.0, y * 16.0 + 8.0)
	return p.distance_to(GRAF_POS) < GRAF_CLEAR_RADIUS

func _in_head_clearing(x: int, y: int) -> bool:
	var p := Vector2(x * 16.0 + 8.0, y * 16.0 + 8.0)
	return p.distance_to(HEAD_POS) < 40.0

func _in_owl_tree_clearing(x: int, y: int) -> bool:
	var p := Vector2(x * 16.0 + 8.0, y * 16.0 + 8.0)
	return p.distance_to(OWL_TREE_POS) < 45.0

func _in_candy_clearing(x: int, y: int) -> bool:
	var p := Vector2(x * 16.0 + 8.0, y * 16.0 + 8.0)
	return p.distance_to(CANDY_POS) < 28.0

func _in_self_clearing(x: int, y: int) -> bool:
	var p := Vector2(x * 16.0 + 8.0, y * 16.0 + 8.0)
	return p.distance_to(SELF_POS) < SELF_CLEAR_RADIUS

func _in_clear_zone(x: int, y: int) -> bool:
	var c := Vector2(MAP_W / 2.0 * 16.0, MAP_H / 2.0 * 16.0)
	var p := Vector2(x * 16.0 + 8.0, y * 16.0 + 8.0)
	return p.distance_to(c) < CLEAR_RADIUS * 16.0
