extends Interactable

func make_friendly() -> void:
	$Sprite2D.visible = false
	$FriendlySprite.visible = true
	text = "good job."
