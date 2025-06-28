from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from perlin_noise import PerlinNoise
import random
import math

noise = PerlinNoise(octaves=3, seed=random.randint(1, 1000000))

app = Ursina()

selected_block = "grass"

player = FirstPersonController(
    mouse_sensitivity=Vec2(100, 100),
    position=(0, 5, 0)
)

block_textures = {
    "grass": load_texture("assets/textures/groundEarth.png"),
    "dirt": load_texture("assets/textures/groundMud.png"),
    "stone": load_texture("assets/textures/wallStone.png"),
    "bedrock": load_texture("assets/textures/stone07.png"),
    "groundCheckered": load_texture("assets/textures/groundCheckered.png"),
    "groundEarth": load_texture("assets/textures/groundEarth.png"),
    "ground": load_texture("assets/textures/ground.png"),
    "ice01": load_texture("assets/textures/ice01.png"),
    "snow": load_texture("assets/textures/snow.png"),
    "Stone02": load_texture("assets/textures/Stone02.png"),
    "stone04": load_texture("assets/textures/stone04.png"),
    "stone06": load_texture("assets/textures/stone06.png"),
    "wallBrick01": load_texture("assets/textures/wallBrick01.png"),
    "wallBrick03": load_texture("assets/textures/wallBrick03.png"),
    "wallBrick05": load_texture("assets/textures/wallBrick05.png"),
    "wallStone": load_texture("assets/textures/wallStone.png"),
    "groundEarthCheckered": load_texture("assets/textures/groundEarthCheckered.png"),
    "groundMud": load_texture("assets/textures/groundMud.png"),
    "groundSnow": load_texture("assets/textures/groundSnow.png"),
    "lava01": load_texture("assets/textures/lava01.png"),
    "Stone01": load_texture("assets/textures/Stone01.png"),
    "Stone03": load_texture("assets/textures/Stone03.png"),
    "stone05": load_texture("assets/textures/stone05.png"),
    "stone07": load_texture("assets/textures/stone07.png"),
    "wallBrick02": load_texture("assets/textures/wallBrick02.png"),
    "wallBrick04": load_texture("assets/textures/wallBrick04.png"),
    "wallBrick06": load_texture("assets/textures/wallBrick06.png"),
    "water": load_texture("assets/textures/water.png")
}

class Block(Entity):
    def __init__(self, position, block_type):
        super().__init__(
            position=position,
            model="assets/models/block_model",
            scale=1,
            origin_y=-0.5,
            texture=block_textures.get(block_type),
            collider="box"
        )
        self.block_type = block_type

mini_block = Entity(
    parent=camera,
    model="assets/models/block_model",
    texture=block_textures.get(selected_block),
    scale=0.2,
    position=(0.35, -0.25, 0.5),
    rotation=(-15, -30, -5)
)

min_height = -5

# Wir speichern Blöcke in einem Dict mit Position als Key, um doppelte Erzeugung zu verhindern
world_blocks = {}

# Chunk- oder Bereichsgröße um den Spieler, in Blöcken
VIEW_DISTANCE = 15  # Radius in x,z Richtung, wie weit Blöcke um den Spieler generiert werden

def generate_block_column(x, z):
    """Generiert eine Block-Säule an Position (x,z) basierend auf Perlin Noise."""
    height_noise = noise([x * 0.02, z * 0.02])
    height = math.floor(height_noise * 7.5)
    # Blöcke von min_height bis Höhe generieren
    for y in range(min_height, height + min_height + 1):
        pos = (x, y, z)
        if pos in world_blocks:
            continue  # Block existiert schon
        if y == min_height:
            block_type = "bedrock"
        elif y == height + min_height:
            block_type = "grass"
        elif (height + min_height) - y > 2:
            block_type = "stone"
        else:
            block_type = "dirt"
        block = Block(pos, block_type)
        world_blocks[pos] = block

def generate_initial_world():
    # Generiere zu Beginn ein Rechteck um (0,0) im Bereich VIEW_DISTANCE
    for x in range(-VIEW_DISTANCE, VIEW_DISTANCE):
        for z in range(-VIEW_DISTANCE, VIEW_DISTANCE):
            generate_block_column(x, z)

# Initiale Welt generieren
generate_initial_world()

def input(key):
    global selected_block
    if key == 'left mouse down':
        hit_info = raycast(camera.world_position, camera.forward, distance=10)
        if hit_info.hit:
            pos = hit_info.entity.position + hit_info.normal
            if pos not in world_blocks:
                block = Block(pos, selected_block)
                world_blocks[pos] = block
    if key == 'right mouse down' and mouse.hovered_entity:
        if not mouse.hovered_entity.block_type == "bedrock":
            pos = mouse.hovered_entity.position
            destroy(mouse.hovered_entity)
            if pos in world_blocks:
                del world_blocks[pos]
    if key == '1':
        selected_block = "grass"
    if key == '2':
        selected_block = "dirt"
    if key == '3':
        selected_block = "stone"
    if key == '4':
        selected_block = "bedrock"
    if key == '5':
        selected_block = "groundCheckered"
    if key == '6':
        selected_block = "groundEarth"
    if key == '7':
        selected_block = "ground"
    if key == '8':
        selected_block = "ice01"
    if key == '9':
        selected_block = "snow"
    if key == '0':
        selected_block = "Stone02"

    # Weiter mit q + Zahl
    if key == 'q1':
        selected_block = "stone04"
    if key == 'q2':
        selected_block = "stone06"
    if key == 'q3':
        selected_block = "wallBrick01"
    if key == 'q4':
        selected_block = "wallBrick03"
    if key == 'q5':
        selected_block = "wallBrick05"
    if key == 'q6':
        selected_block = "wallStone"
    if key == 'q7':
        selected_block = "groundEarthCheckered"
    if key == 'q8':
        selected_block = "groundMud"
    if key == 'q9':
        selected_block = "groundSnow"
    if key == 'q0':
        selected_block = "lava01"

    # Noch weiter mit anderen q + Zahl Kombinationen:
    if key == '11':
        selected_block = "Stone01"
    if key == '12':
        selected_block = "Stone03"
    if key == '13':
        selected_block = "stone05"
    if key == '14':
        selected_block = "stone07"
    if key == '15':
        selected_block = "wallBrick02"
    if key == '16':
        selected_block = "wallBrick04"
    if key == '17':
        selected_block = "wallBrick06"
    if key == '18':
        selected_block = "water"


last_player_chunk = (None, None)

def update():
    global last_player_chunk
    mini_block.texture = block_textures.get(selected_block)

    # Ermittle aktuelle Chunk-Position (x,z)
    player_chunk_x = round(player.x)
    player_chunk_z = round(player.z)

    # Nur wenn der Spieler sich in einem neuen Chunk befindet, Welt erweitern
    if (player_chunk_x, player_chunk_z) != last_player_chunk:
        last_player_chunk = (player_chunk_x, player_chunk_z)

        # Generiere Blöcke um den Spieler in einem Radius VIEW_DISTANCE
        for x in range(player_chunk_x - VIEW_DISTANCE, player_chunk_x + VIEW_DISTANCE):
            for z in range(player_chunk_z - VIEW_DISTANCE, player_chunk_z + VIEW_DISTANCE):
                generate_block_column(x, z)

        # Optional: Entferne Blöcke, die zu weit entfernt sind, um Speicher zu sparen
        to_remove = []
        for pos in world_blocks:
            x, y, z = pos
            if abs(x - player_chunk_x) > VIEW_DISTANCE + 5 or abs(z - player_chunk_z) > VIEW_DISTANCE + 5:
                to_remove.append(pos)
        for pos in to_remove:
            destroy(world_blocks[pos])
            del world_blocks[pos]

app.run()
