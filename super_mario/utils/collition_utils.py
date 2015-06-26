__author__ = 'bakeneko'


LEFT, TOP, RIGHT, BOTTOM, CENTER = range(5)


def collide_block_position(sprite_rect, brick_rect):
    collision = [False] * 9

    collision[0] = sprite_rect.collidepoint(brick_rect.topleft)
    collision[1] = sprite_rect.collidepoint(brick_rect.topright)
    collision[2] = sprite_rect.collidepoint(brick_rect.bottomleft)
    collision[3] = sprite_rect.collidepoint(brick_rect.bottomright)

    collision[4] = sprite_rect.collidepoint(brick_rect.midleft)
    collision[5] = sprite_rect.collidepoint(brick_rect.midright)
    collision[6] = sprite_rect.collidepoint(brick_rect.midtop)
    collision[7] = sprite_rect.collidepoint(brick_rect.midbottom)

    collision[8] = sprite_rect.collidepoint(brick_rect.center)

    SIZE = []
    if collision[4] or collision[0] or collision[2]:
        SIZE.append(LEFT)

    if collision[0] or collision[1] or collision[6]:
        SIZE.append(TOP)

    if collision[1] or collision[3] or collision[5]:
        SIZE.append(RIGHT)

    if collision[2] or collision[3] or collision[7]:
        SIZE.append(BOTTOM)

    if collision[8]:
        SIZE.append(CENTER)

    return SIZE