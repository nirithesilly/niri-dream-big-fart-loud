extends Node

const GAME_OVER_SCENE := preload("res://scenes/ui/GameOver.tscn")

var game_over := false
var head_resolved := false
var good_ending := false
var has_candy := false


func trigger_game_over() -> void:
	if game_over:
		return
	game_over = true
	get_tree().root.add_child(GAME_OVER_SCENE.instantiate())
	get_tree().paused = true


func resolve_good_ending() -> void:
	if head_resolved or game_over:
		return
	head_resolved = true
	good_ending = true
	var head := get_tree().get_first_node_in_group("baby_head")
	if head:
		head.queue_free()
	var owl := get_tree().get_first_node_in_group("owl")
	if owl:
		owl.queue_free()
	var wolf := get_tree().get_first_node_in_group("wolf")
	if wolf and wolf.has_method("make_friendly"):
		wolf.make_friendly()


func resolve_head() -> void:
	if head_resolved or game_over:
		return
	head_resolved = true
	var head := get_tree().get_first_node_in_group("baby_head")
	if head:
		head.queue_free()
	var wolf := get_tree().get_first_node_in_group("wolf")
	var owl := get_tree().get_first_node_in_group("owl")
	if owl != null and owl.landed:
		good_ending = true
		if wolf and wolf.has_method("make_friendly"):
			wolf.make_friendly()
		if owl.has_method("close_eyes"):
			owl.close_eyes()
	else:
		if wolf:
			wolf.queue_free()
		for sheep in get_tree().get_nodes_in_group("sheep"):
			if sheep.has_method("scatter"):
				sheep.scatter()
		if owl != null and owl.has_method("mark_blame"):
			owl.mark_blame()
