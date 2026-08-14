extends CanvasLayer

const MARGIN_L := 28.0 #отступ слева
const MARGIN_R := -28.0 #отступ справа
const MARGIN_T := -60.0 #отступ сверху (низ окна от нижнего края экрана)
const MARGIN_B := -16.0 #отступ снизу
const CHOICE_EXTRA := 50.0 #насколько окно поднимается выше при выборе

var box: Panel
var label: Label

var _shown := false
var _queue: Array[String] = []
var _on_finished: Callable = Callable()
var _options: Array[String] = []
var _sel := 0
var _on_pick: Callable = Callable()
var _message := ""


func _ready() -> void:
	layer = 10
	box = Panel.new()
	box.anchor_left = 0.0
	box.anchor_right = 1.0
	box.anchor_top = 1.0
	box.anchor_bottom = 1.0
	box.offset_left = MARGIN_L
	box.offset_right = MARGIN_R
	box.offset_top = MARGIN_T
	box.offset_bottom = MARGIN_B
	var sb := StyleBoxFlat.new()
	sb.bg_color = Color(0.06, 0.06, 0.08, 0.95)
	sb.border_color = Color(0.5, 0.5, 0.56)
	sb.set_border_width_all(1)
	sb.set_content_margin_all(6)
	box.add_theme_stylebox_override("panel", sb)
	add_child(box)
	label = Label.new()
	label.set_anchors_preset(Control.PRESET_FULL_RECT)
	label.offset_left = 8.0
	label.offset_right = -8.0
	label.offset_top = 2.0
	label.offset_bottom = -2.0
	label.add_theme_font_size_override("font_size", 9)
	label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	label.vertical_alignment = VERTICAL_ALIGNMENT_CENTER
	box.add_child(label)
	box.visible = false

func show_message(text: String) -> void:
	_queue = []
	_on_finished = Callable()
	_reset_choices()
	_message = text
	label.text = text
	box.visible = true
	_shown = true


func show_sequence(messages: Array, on_finished: Callable = Callable()) -> void:
	_queue.assign(messages)
	_on_finished = on_finished
	_reset_choices()
	_show_next()


func show_choices(message: String, options: Array, on_pick: Callable) -> void:
	_queue = []
	_on_finished = Callable()
	_options.assign(options)
	_sel = 0
	_on_pick = on_pick
	_message = message
	box.offset_top = MARGIN_T - CHOICE_EXTRA
	_redraw_choices()
	box.visible = true
	_shown = true


func is_shown() -> bool:
	return _shown


func _redraw_choices() -> void:
	var lines := PackedStringArray()
	for i in _options.size():
		var prefix := "> " if i == _sel else "  "
		lines.append(prefix + _options[i])
	label.text = _message + "\n\n" + "\n".join(lines)


func _reset_choices() -> void:
	_options = []
	_sel = 0
	_on_pick = Callable()
	box.offset_top = MARGIN_T


func _show_next() -> void:
	if _queue.is_empty():
		box.visible = false
		_shown = false
		if _on_finished.is_valid():
			var cb := _on_finished
			_on_finished = Callable()
			cb.call()
		return
	_message = _queue.pop_front()
	label.text = _message
	box.visible = true
	_shown = true


func _unhandled_input(event: InputEvent) -> void:
	if not _shown:
		return
	if not _options.is_empty():
		if event.is_action_pressed("ui_up"):
			_sel = (_sel + _options.size() - 1) % _options.size()
			_redraw_choices()
			get_viewport().set_input_as_handled()
		elif event.is_action_pressed("ui_down"):
			_sel = (_sel + 1) % _options.size()
			_redraw_choices()
			get_viewport().set_input_as_handled()
		elif event.is_action_pressed("ui_accept"):
			var pick := _on_pick
			var picked := _sel
			_reset_choices()
			box.visible = false
			_shown = false
			if pick.is_valid():
				pick.call(picked)
			get_viewport().set_input_as_handled()
	elif event.is_action_pressed("ui_accept"):
		_show_next()
		get_viewport().set_input_as_handled()
