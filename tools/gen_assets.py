import os
import random
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "assets")
SPRITES = os.path.join(ASSETS, "sprites")
RESOURCES = os.path.join(ASSETS, "resources")
os.makedirs(SPRITES, exist_ok=True)
os.makedirs(RESOURCES, exist_ok=True)

HAIR    = (18, 18, 22)
HAIR_HI = (44, 44, 54)
SKIN    = (232, 214, 196)
SKIN_SH = (172, 144, 118)
EYE     = (150, 130, 108)
PONCHO  = (34, 34, 42)
FOLD    = (48, 48, 58)
EDGE    = (14, 14, 18)
SCARF   = (184, 56, 52)
SCARF_D = (122, 34, 30)
SCARF_H = (214, 74, 64)
SHOE    = (16, 16, 20)
SHOE_HI = (40, 40, 48)
GRAY    = (178, 178, 190)
GRAY_D  = (150, 150, 164)

PAL = {
    ".": None,
    "H": HAIR,    "h": HAIR_HI,
    "S": SKIN,    "s": SKIN_SH,
    "e": EYE,
    "g": GRAY,    "w": GRAY_D,
    "P": PONCHO,  "p": FOLD, "E": EDGE,
    "R": SCARF,   "r": SCARF_D, "t": SCARF_H,
    "B": SHOE,    "b": SHOE_HI,
}

def row(*cells):
    assert len(cells) == 16, cells
    return list(cells)

def full_hair_row():
    return row(".", *(["H"] * 14), ".")

def front_face_row():
    return row(".", "H", "g", *(["S"] * 10), "g", "H", ".")

def front_eye_row():
    return row(".", "H", "g", "S", "S", "e", "e", "S", "S", "e", "e", "S", "S", "g", "H", ".")

def front_chin_row():
    return row(".", "h", "H", "g", *(["S"] * 8), "g", "H", "h", ".")

def scarf_row():
    return row(".", "h", "h", *(["R"] * 10), "h", "h", ".")

def back_hair_hi_row():
    return row(".", *(["H"] * 7), "h", *(["H"] * 6), ".")

def back_hair_nape_row():
    return row(".", "H", "H", "H", "H", "g", "g", "H", "H", "g", "g", "H", "H", "H", "H", ".")

def back_chin_row():
    return row(".", "h", "H", "H", "H", "g", "g", "H", "H", "g", "g", "H", "H", "H", "h", ".")

def left_face_row():
    return row(".", "h", "H", "g", *(["S"] * 5), *(["H"] * 6), ".")

def left_eye_row():
    return row(".", "h", "H", "g", "S", "S", "e", "e", "S", *(["H"] * 6), ".")

def left_chin_row():
    return row(".", "h", "H", "g", *(["S"] * 4), "h", *(["H"] * 5), "g", ".")

def left_scarf_row():
    return row(".", "h", "H", "r", *(["R"] * 4), "r", *(["H"] * 6), ".")

HEAD_FRONT = (
    [full_hair_row() for _ in range(8)]
    + [front_face_row(), front_eye_row(), front_face_row(),
       front_face_row(), front_face_row(), front_chin_row(),
       scarf_row(), scarf_row()]
)

HEAD_BACK = (
    [full_hair_row() for _ in range(8)]
    + [back_hair_hi_row(), full_hair_row(), back_hair_hi_row(),
       back_hair_nape_row(), back_hair_nape_row(), back_chin_row(),
       scarf_row(), scarf_row()]
)

HEAD_LEFT = (
    [full_hair_row() for _ in range(8)]
    + [left_face_row(), left_eye_row(), left_face_row(),
       left_face_row(), left_face_row(), left_chin_row(),
       left_scarf_row(), left_scarf_row()]
)

def mirror_rows(rows):
    return [list(reversed(r)) for r in rows]

HEAD_RIGHT = mirror_rows(HEAD_LEFT)
HEADS = {"down": HEAD_FRONT, "up": HEAD_BACK, "left": HEAD_LEFT, "right": HEAD_RIGHT}


def poncho_y(y):
    """left/right column of the poncho silhouette for a given row."""
    t = (y - 16) / 12.0
    left = round(4 + (1 - 4) * t)
    right = round(11 + (14 - 11) * t)
    return left, right


def stamp_tail(g, direction):
    if direction == "left":
        cx = 12
    elif direction == "right":
        cx = 3
    else:
        cx = 2 if direction == "down" else 12
    g[17][cx] = SCARF; g[17][cx + 1] = SCARF
    g[18][cx] = SCARF; g[18][cx + 1] = SCARF_D
    g[19][cx] = SCARF; g[19][cx + 1] = SCARF_D
    g[20][cx] = SCARF_D
    g[21][cx] = SCARF_D
    g[22][cx] = SCARF_D


def stamp_shoes(g, direction, pose):
    if direction in ("down", "up"):
        a, b = (6, 7), (9, 10)
    else:
        a, b = (5, 6), (8, 9)
    if pose == "idle":
        ra, rb = (29, 30), (29, 30)
    elif pose == "walk1":
        ra, rb = (29, 30), (30, 31)
    else:
        ra, rb = (30, 31), (29, 30)
    for cols, rows in ((a, ra), (b, rb)):
        for dx in range(2):
            g[rows[0]][cols[0] + dx] = SHOE_HI
            g[rows[1]][cols[0] + dx] = SHOE


def build_frame(direction, pose):
    g = [[None] * 16 for _ in range(32)]
    for y, cells in enumerate(HEADS[direction]):
        for x, ch in enumerate(cells):
            g[y][x] = PAL[ch]
    for y in range(16, 29):
        left, right = poncho_y(y)
        for x in range(left, right + 1):
            g[y][x] = PONCHO
        g[y][left] = EDGE
        g[y][right] = EDGE
        for x in range(left + 2, right, 3):
            g[y][x] = FOLD
    y = 28
    left, right = poncho_y(y)
    for x in range(left, right + 1):
        g[y][x] = PONCHO if x == left or x == right else EDGE
    stamp_tail(g, direction)
    stamp_shoes(g, direction, pose)
    if pose != "idle":
        out = [[None] * 16 for _ in range(32)]
        for y in range(31):
            out[y + 1] = g[y]
        g = out
    return g


ORDER = [
    ("down", "idle"), ("down", "walk1"), ("down", "walk2"),
    ("up", "idle"), ("up", "walk1"), ("up", "walk2"),
    ("left", "idle"), ("left", "walk1"), ("left", "walk2"),
    ("right", "idle"), ("right", "walk1"), ("right", "walk2"),
]


def gen_roma():
    sheet = Image.new("RGBA", (16 * 3, 32 * 4), (0, 0, 0, 0))
    spx = sheet.load()
    for i, (direction, pose) in enumerate(ORDER):
        ox = (i % 3) * 16
        oy = (i // 3) * 32
        frame = build_frame(direction, pose)
        for y in range(32):
            for x in range(16):
                c = frame[y][x]
                if c:
                    spx[ox + x, oy + y] = c
    sheet.save(os.path.join(SPRITES, "roma.png"))
    print("roma.png")


def gen_tree():
    tw, th = 48, 64
    img = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    spx = img.load()
    rnd = random.Random(7)

    mask = [[False] * tw for _ in range(42)]
    blobs = [
        (24, 16, 16), (10, 20, 10), (38, 20, 10), (24, 6, 11),
        (16, 28, 8), (32, 28, 8), (24, 35, 6), (6, 10, 6), (42, 10, 6),
    ]
    for cx, cy, r in blobs:
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if 0 <= yy < 42 and 0 <= xx < tw and (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    mask[yy][xx] = True

    LEAF = (74, 52, 112)
    LEAF_DK = (46, 31, 69)
    LEAF_LT = (93, 68, 144)
    LEAF_HI = (122, 95, 176)
    for yy in range(42):
        for xx in range(tw):
            if not mask[yy][xx]:
                continue
            edge = any(
                xx + dx < 0 or xx + dx >= tw or yy + dy < 0 or yy + dy >= 42 or not mask[yy + dy][xx + dx]
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
            )
            c = LEAF_DK if edge else LEAF
            if not edge and rnd.random() < 0.05:
                c = LEAF_LT
            if not edge and rnd.random() < 0.03 and yy < 12:
                c = LEAF_HI
            spx[xx, yy] = c

    TRUNK = (70, 84, 107)
    TRUNK_DK = (58, 70, 92)
    TRUNK_LT = (90, 106, 134)
    for yy in range(32, 64):
        half = 3 + int((yy - 32) / 31 * 2)
        for xx in range(24 - half, 24 + half):
            c = TRUNK_LT if xx < 24 - half + 1 else (TRUNK_DK if xx > 24 + half - 2 else TRUNK)
            spx[xx, yy] = c

    img.save(os.path.join(SPRITES, "tree.png"))
    print("tree.png")


def gen_grass():
    cols, rows = 4, 2
    ts = 16
    img = Image.new("RGBA", (cols * ts, rows * ts), (0, 0, 0, 0))
    spx = img.load()
    rnd = random.Random(13)
    BASE = (26, 26, 28)
    NOISE = (38, 38, 42)
    TUFT = (58, 58, 66)
    TUFT_T = (70, 70, 80)
    for ty in range(rows):
        for tx in range(cols):
            for y in range(ts):
                for x in range(ts):
                    spx[tx * ts + x, ty * ts + y] = BASE
            # sparse light noise
            for _ in range(rnd.randint(2, 4)):
                spx[tx * ts + rnd.randrange(ts), ty * ts + rnd.randrange(ts)] = NOISE
            # grass tufts
            for _ in range(rnd.randint(0, 2)):
                x = rnd.randrange(2, ts - 3)
                y = rnd.randrange(3, ts - 3)
                spx[tx * ts + x, ty * ts + y] = TUFT
                spx[tx * ts + x + 1, ty * ts + y - 1] = TUFT_T
                if rnd.random() < 0.5:
                    spx[tx * ts + x - 1, ty * ts + y] = TUFT
    img.save(os.path.join(SPRITES, "grass.png"))
    print("grass.png")


def gen_roma_tres():
    lines = []
    lines.append('[gd_resource type="SpriteFrames" load_steps=13 format=3]')
    lines.append("")
    lines.append('[ext_resource type="Texture2D" path="res://assets/sprites/roma.png" id="1"]')
    lines.append("")
    for i in range(12):
        ox = (i % 3) * 16
        oy = (i // 3) * 32
        lines.append(f'[sub_resource type="AtlasTexture" id="AtlasTexture_{i}"]')
        lines.append('atlas = ExtResource("1")')
        lines.append(f"region = Rect2({ox}, {oy}, 16, 32)")
        lines.append("")
    anims = []
    for name, idxs, speed in [
        ("down_idle", [0], 1.0), ("down_walk", [1, 2], 6.0),
        ("up_idle", [3], 1.0), ("up_walk", [4, 5], 6.0),
        ("left_idle", [6], 1.0), ("left_walk", [7, 8], 6.0),
        ("right_idle", [9], 1.0), ("right_walk", [10, 11], 6.0),
    ]:
        frames = ", ".join(f'SubResource("AtlasTexture_{i}")' for i in idxs)
        anims.append(
            f'{{"frames": [{frames}], "loop": true, "name": &"{name}", "speed": {speed}, "tint": Color(1, 1, 1, 1)}}'
        )
    lines.append("[resource]")
    lines.append(f"animations = [")
    for a in anims:
        lines.append(a + ",")
    lines.append("]")
    with open(os.path.join(RESOURCES, "roma_frames.tres"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print("roma_frames.tres")


def gen_grass_tres():
    lines = []
    lines.append('[gd_resource type="TileSet" load_steps=3 format=3]')
    lines.append("")
    lines.append('[ext_resource type="Texture2D" path="res://assets/sprites/grass.png" id="1"]')
    lines.append("")
    lines.append('[sub_resource type="TileSetAtlasSource" id="TileSetAtlasSource_1"]')
    lines.append('texture = ExtResource("1")')
    lines.append("texture_region_size = Vector2i(16, 16)")
    for ty in range(2):
        for tx in range(4):
            lines.append(f"{tx}:{ty}/0 = 0")
    lines.append("")
    lines.append("[resource]")
    lines.append("tile_size = Vector2i(16, 16)")
    lines.append('sources/0 = SubResource("TileSetAtlasSource_1")')
    with open(os.path.join(RESOURCES, "grass.tres"), "w") as f:
        f.write("\n".join(lines) + "\n")
    print("grass.tres")


def _ellipse(spx, tw, th, cx, cy, rx, ry, col):
    for y in range(max(0, cy - ry), min(th, cy + ry + 1)):
        for x in range(max(0, cx - rx), min(tw, cx + rx + 1)):
            if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0:
                spx[x, y] = col


def _tri(spx, tw, th, x0, y0, h, col):
    for yy in range(h):
        half = yy // 2 + 1
        for xx in range(x0 - half + 1, x0 + half):
            if 0 <= xx < tw and 0 <= y0 + yy < th:
                spx[xx, y0 + yy] = col


def gen_graf():
    tw, th = 40, 28
    img = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    spx = img.load()
    rnd = random.Random(5)
    B = (40, 37, 46)
    BD = (26, 24, 33)
    BK = (15, 14, 20)
    EYE = (238, 234, 244)
    TOOTH = (228, 228, 234)
    BLOOD = (150, 22, 28)
    BLOOD_D = (110, 16, 22)
    BLOOD_H = (196, 44, 50)
    MOUTH = (22, 11, 15)

    def ell(cx, cy, rx, ry, col):
        for y in range(max(0, cy - ry), min(th, cy + ry + 1)):
            for x in range(max(0, cx - rx), min(tw, cx + rx + 1)):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0:
                    spx[x, y] = col

    def tri(x0, y0, h, col):
        for yy in range(h):
            half = yy // 2 + 1
            for xx in range(x0 - half + 1, x0 + half):
                if 0 <= xx < tw and 0 <= y0 + yy < th:
                    spx[xx, y0 + yy] = col

    # tail curling up behind
    ell(7, 21, 4, 2, B)
    ell(5, 18, 2, 2, BD)
    ell(8, 23, 3, 1, BD)
    # body with hunched back
    ell(20, 18, 12, 5, B)
    ell(19, 20, 10, 4, BD)
    ell(29, 15, 5, 4, B)
    # creepy ribs poking through
    for rx in (13, 17, 21, 25):
        for yy in (16, 17):
            if 0 <= rx < tw and 0 <= yy < th:
                spx[rx, yy] = BK
    # scratches on the flank
    for sx, sy in ((14, 20), (17, 22), (20, 20)):
        if 0 <= sx < tw and 0 <= sy < th:
            spx[sx, sy] = BK
    # hind leg
    ell(11, 23, 3, 4, B)
    # front legs
    ell(24, 23, 3, 4, B)
    ell(30, 23, 3, 4, B)
    for fx in (11, 24, 30):
        ell(fx, 27, 3, 1, BD)
    # neck / chest
    ell(31, 16, 5, 5, B)
    ell(31, 19, 4, 3, BD)
    # head
    ell(34, 11, 7, 6, B)
    ell(35, 14, 5, 3, BD)
    # big open maw
    for yy in (13, 14):
        for xx in range(31, tw):
            spx[xx, yy] = MOUTH
    # teeth
    for xx in (33, 35, 37, 39):
        spx[xx, 12] = TOOTH
    for xx in (34, 36, 38):
        spx[xx, 15] = TOOTH
    # pointed ear
    tri(30, 3, 5, B)
    tri(31, 4, 3, BD)
    # sunken pale eye
    spx[32, 8] = BK
    spx[33, 8] = BK
    spx[32, 7] = EYE
    spx[33, 7] = EYE
    # blood dripping from the maw
    for col in (33, 36, 38):
        yy = 16
        while yy < 25 and rnd.random() < 0.9:
            spx[col, yy] = BLOOD if yy < 22 else BLOOD_D
            yy += 1
            if rnd.random() < 0.4:
                break
        if yy < 25 and rnd.random() < 0.6:
            spx[col, yy] = BLOOD_D
    for col in (33, 36, 38):
        spx[col, 16] = BLOOD_H
    img.save(os.path.join(SPRITES, "graf.png"))
    print("graf.png")


SHEEP_GRID = [
    "..........HHHHHH.......",
    ".........HHHHHEHHHH.....",
    ".........HHHHHHHHHPP...",
    "........HHHHHHHHHPP....",
    ".......HHHHHHHHHHHH....",
    "......WWWWWWWWWWWWWW...",
    ".....WWWWWWWWWWWWWWW..",
    "....WWWWWWWWWWWWWWWW..",
    "....WWWWWWWWWWWWWWWW..",
    "....WWWWWWWWWWWWWWWW..",
    "....wwWWWWWWWWWWwwWW..",
    ".....wwwwwwwwwwwwwww..",
    "......LL...LL..LL...LL",
    "......LL...LL..LL...LL",
]


def gen_sheep():
    tw, th = 22, 14
    img = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    spx = img.load()
    rnd = random.Random(9)
    cols = {
        "H": (98, 98, 114),
        "E": (26, 26, 34),
        "P": (150, 120, 132),
        "W": (238, 238, 244),
        "w": (205, 205, 216),
        "L": (112, 112, 124),
    }
    for y, row in enumerate(SHEEP_GRID):
        for x, ch in enumerate(row):
            c = cols.get(ch)
            if c:
                spx[x, y] = c
    # fluffy wool bumps along the top edge
    for x in range(6, 18):
        if spx[x, 5] == cols["W"] and spx[x, 4][3] == 0 and rnd.random() < 0.5:
            spx[x, 4] = cols["W"]
    img.save(os.path.join(SPRITES, "sheep.png"))
    print("sheep.png")


def gen_baby_head():
    tw, th = 24, 24
    img = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    spx = img.load()
    rnd = random.Random(21)
    H  = (18, 17, 26)
    h  = (42, 40, 54)
    S  = (230, 218, 206)
    S2 = (246, 238, 228)
    s  = (172, 152, 138)
    s2 = (118, 100, 88)
    E  = (24, 20, 30)
    p  = (216, 210, 222)
    M  = (50, 20, 26)
    M2 = (20, 10, 14)
    V  = (158, 130, 140)
    B  = (130, 40, 44)
    B2 = (172, 54, 58)
    G  = (98, 40, 46)
    G2 = (64, 26, 32)

    def stamp(x, y, c):
        if 0 <= x < tw and 0 <= y < th:
            spx[x, y] = c

    # round skull
    for y in range(th):
        for x in range(tw):
            if (x - 11) ** 2 + (y - 11) ** 2 <= 121:
                spx[x, y] = S

    # subtle mottled skin
    for y in range(3, 17):
        for x in range(tw):
            if spx[x, y] == S:
                r = rnd.random()
                if r < 0.04:
                    spx[x, y] = S2
                elif r < 0.065:
                    spx[x, y] = s

    # baby fuzz: a small crown tuft sticking up
    for x, y in ((10, 0), (11, 0), (12, 0), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1), (4, 3), (5, 3), (18, 3), (19, 3)):
        stamp(x, y, H)
    stamp(11, 0, h)
    stamp(11, 1, h)

    # rounded shading: bright crown, darker sides and bottom
    for x in range(7, 17):
        stamp(x, 3, S2)
    for x in range(9, 14):
        stamp(x, 4, S2)
    for x in range(1, 6):
        stamp(x, 12, s)
    for x in range(18, 23):
        stamp(x, 12, s)
    for y in range(7, 14):
        stamp(22, y, s)
        stamp(23, y, s2)
    for y in range(16, 22):
        for x in range(tw):
            if spx[x, y] == S:
                spx[x, y] = s if y < 19 else s2

    # big wide-set baby eyes, low on the face
    for x in range(6, 9):
        for y in range(10, 12):
            stamp(x, y, E)
    for x in range(15, 18):
        for y in range(10, 12):
            stamp(x, y, E)
    stamp(7, 10, p)
    stamp(16, 10, p)
    # dark circles under the eyes
    for x in range(6, 9):
        stamp(x, 12, s2)
    for x in range(15, 18):
        stamp(x, 12, s2)
    # a tear from the right eye
    stamp(17, 13, B)
    stamp(17, 14, B2)
    stamp(18, 15, B2)
    # faint temple veins
    stamp(3, 9, V)
    stamp(4, 9, V)
    stamp(20, 9, V)
    stamp(19, 9, V)

    # tiny nose bump
    stamp(11, 12, s2)
    stamp(11, 13, s)

    # small slightly open mouth with a blood drop in the corner
    for x in range(10, 13):
        stamp(x, 14, M)
        stamp(x, 15, M2)
    stamp(10, 15, M)
    stamp(12, 15, M)
    stamp(13, 14, B2)
    stamp(13, 15, B)

    # chubby cheek highlights
    stamp(4, 11, S2)
    stamp(5, 12, S2)
    stamp(19, 11, S2)
    stamp(18, 12, S2)

    # small ragged cut at the bottom (the neck stump)
    for x, y in ((10, 20), (11, 20), (12, 20), (11, 21)):
        stamp(x, y, G2)
    stamp(10, 21, G)

    img.save(os.path.join(SPRITES, "baby_head.png"))
    print("baby_head.png")


def gen_friendly_graf():
    tw, th = 40, 28
    img = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    spx = img.load()
    B = (40, 37, 46)
    BD = (26, 24, 33)
    BK = (15, 14, 20)
    EYE = (238, 234, 244)
    MOUTH = (22, 11, 15)

    def ell(cx, cy, rx, ry, col):
        for y in range(max(0, cy - ry), min(th, cy + ry + 1)):
            for x in range(max(0, cx - rx), min(tw, cx + rx + 1)):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0:
                    spx[x, y] = col

    def tri(x0, y0, h, col):
        for yy in range(h):
            half = yy // 2 + 1
            for xx in range(x0 - half + 1, x0 + half):
                if 0 <= xx < tw and 0 <= y0 + yy < th:
                    spx[xx, y0 + yy] = col

    # same hunched silhouette, same dark colors - just no gore
    ell(7, 21, 4, 2, B)
    ell(5, 18, 2, 2, BD)
    ell(8, 23, 3, 1, BD)
    ell(20, 18, 12, 5, B)
    ell(19, 20, 10, 4, BD)
    ell(29, 15, 5, 4, B)
    ell(11, 23, 3, 4, B)
    ell(24, 23, 3, 4, B)
    ell(30, 23, 3, 4, B)
    for fx in (11, 24, 30):
        ell(fx, 27, 3, 1, BD)
    ell(31, 16, 5, 5, B)
    ell(31, 19, 4, 3, BD)
    ell(34, 11, 7, 6, B)
    ell(35, 14, 5, 3, BD)
    tri(30, 3, 5, B)
    tri(31, 4, 3, BD)
    # normal bright eye, no sunken socket
    spx[32, 7] = EYE
    spx[33, 7] = EYE
    spx[32, 8] = BK
    # small calm smile, closed mouth
    spx[34, 14] = MOUTH
    spx[35, 14] = MOUTH
    spx[36, 13] = MOUTH
    img.save(os.path.join(SPRITES, "friendly_graf.png"))
    print("friendly_graf.png")


OWL_ROWS = [
    [(3, "."), (2, "B"), (10, "."), (2, "B"), (3, ".")],
    [(2, "."), (3, "B"), (10, "B"), (3, "B"), (2, ".")],
    [(2, "."), (4, "B"), (8, "B"), (4, "B"), (2, ".")],
    [(2, "."), (4, "B"), (8, "B"), (4, "B"), (2, ".")],
    [(2, "."), (3, "B"), (2, "E"), (6, "B"), (2, "E"), (3, "B"), (2, ".")],
    [(2, "."), (3, "B"), (3, "E"), (4, "B"), (3, "E"), (3, "B"), (2, ".")],
    [(2, "."), (3, "B"), (3, "E"), (1, "P"), (2, "B"), (1, "P"), (3, "E"), (3, "B"), (2, ".")],
    [(2, "."), (3, "B"), (3, "E"), (1, "P"), (2, "B"), (1, "P"), (3, "E"), (3, "B"), (2, ".")],
    [(2, "."), (3, "B"), (2, "E"), (2, "B"), (1, "K"), (2, "B"), (2, "E"), (3, "B"), (2, ".")],
    [(2, "."), (3, "B"), (1, "B"), (2, "B"), (2, "K"), (2, "B"), (2, "B"), (1, "B"), (3, "B"), (2, ".")],
    [(2, "."), (4, "B"), (2, "B"), (4, "V"), (2, "B"), (4, "B"), (2, ".")],
    [(2, "."), (4, "B"), (2, "b"), (4, "V"), (2, "b"), (4, "B"), (2, ".")],
    [(2, "."), (4, "B"), (1, "b"), (6, "V"), (1, "b"), (4, "B"), (2, ".")],
    [(2, "."), (4, "B"), (1, "b"), (3, "V"), (1, "s"), (2, "V"), (1, "b"), (4, "B"), (2, ".")],
    [(2, "."), (4, "B"), (8, "V"), (4, "B"), (2, ".")],
    [(3, "."), (3, "B"), (8, "."), (3, "B"), (3, ".")],
]

OWL_ROWS_CLOSED = [
    [(3, "."), (2, "B"), (10, "."), (2, "B"), (3, ".")],
    [(2, "."), (3, "B"), (10, "B"), (3, "B"), (2, ".")],
    [(2, "."), (4, "B"), (8, "B"), (4, "B"), (2, ".")],
    [(2, "."), (4, "B"), (8, "B"), (4, "B"), (2, ".")],
    [(2, "."), (3, "B"), (2, "B"), (6, "B"), (2, "B"), (3, "B"), (2, ".")],
    [(2, "."), (3, "B"), (3, "B"), (4, "B"), (3, "B"), (3, "B"), (2, ".")],
    [(2, "."), (3, "B"), (2, "B"), (2, "P"), (2, "B"), (2, "P"), (2, "B"), (3, "B"), (2, ".")],
    [(2, "."), (3, "B"), (2, "B"), (2, "P"), (2, "B"), (2, "P"), (2, "B"), (3, "B"), (2, ".")],
    [(2, "."), (3, "B"), (2, "B"), (2, "B"), (1, "K"), (2, "B"), (2, "B"), (3, "B"), (2, ".")],
    [(2, "."), (3, "B"), (1, "B"), (2, "B"), (2, "K"), (2, "B"), (2, "B"), (1, "B"), (3, "B"), (2, ".")],
    [(2, "."), (4, "B"), (2, "B"), (4, "V"), (2, "B"), (4, "B"), (2, ".")],
    [(2, "."), (4, "B"), (2, "b"), (4, "V"), (2, "b"), (4, "B"), (2, ".")],
    [(2, "."), (4, "B"), (1, "b"), (6, "V"), (1, "b"), (4, "B"), (2, ".")],
    [(2, "."), (4, "B"), (1, "b"), (3, "V"), (1, "s"), (2, "V"), (1, "b"), (4, "B"), (2, ".")],
    [(2, "."), (4, "B"), (8, "V"), (4, "B"), (2, ".")],
    [(3, "."), (3, "B"), (8, "."), (3, "B"), (3, ".")],
]

OWL_COLS = {
    "B": (120, 104, 96),
    "b": (100, 86, 80),
    "V": (214, 206, 192),
    "s": (176, 162, 144),
    "E": (240, 216, 128),
    "P": (24, 20, 24),
    "K": (214, 150, 74),
}


def _draw_owl(rows, fname):
    tw, th = 20, 16
    img = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    spx = img.load()
    for y, segs in enumerate(rows):
        x = 0
        for n, ch in segs:
            for _ in range(n):
                c = OWL_COLS.get(ch)
                if c:
                    spx[x, y] = c
                x += 1
    img.save(os.path.join(SPRITES, fname))
    print(fname)


def gen_owl():
    _draw_owl(OWL_ROWS, "owl.png")
    _draw_owl(OWL_ROWS_CLOSED, "owl_closed.png")


CANDY_GRID = [
    "....WWWWWW....",
    "...WWWWWWWW...",
    "..WWWRRRRRRWW.",
    "..WWRRRRRRRRWW",
    "..WWRRRssRRRWW",
    "..WWRRRssRRRWW",
    "..WWRRRRRRRRWW",
    "..WWWRRRRRRWW.",
    "...WWWWWWWW...",
    "....WWWWWW....",
]

CANDY_COLS = {
    "W": (205, 210, 222),
    "R": (192, 60, 70),
    "s": (245, 240, 238),
}


def gen_candy():
    tw, th = 14, 10
    img = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    spx = img.load()
    for y, row in enumerate(CANDY_GRID):
        for x, ch in enumerate(row):
            c = CANDY_COLS.get(ch)
            if c:
                spx[x, y] = c
    img.save(os.path.join(SPRITES, "candy.png"))
    print("candy.png")


def gen_icon():
    """Project/app icon: upscaled down-idle frame of the player (Roma)."""
    sheet = Image.open(os.path.join(SPRITES, "roma.png"))
    frame = sheet.crop((0, 0, 16, 32)).resize((128, 256), Image.NEAREST)
    icon = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    icon.paste(frame, (64, 0))
    icon.save(os.path.join(ROOT, "icon.png"))
    print("icon.png")


if __name__ == "__main__":
    gen_roma()
    gen_tree()
    gen_grass()
    gen_graf()
    gen_sheep()
    gen_baby_head()
    gen_owl()
    gen_friendly_graf()
    gen_candy()
    gen_roma_tres()
    gen_grass_tres()
    gen_icon()
