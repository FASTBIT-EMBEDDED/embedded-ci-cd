/*
 * game.c
 *
 *  Created on: Mar 13, 2026
 *      Author: Shreyas Acharya, Fastbit Embedded
 */

#include "game.h"
#include "world.h"
#include "player.h"
#include "gc9a01a.h"
#include "mpu6050.h"
#include "ball_img.h"

#define LCD_SIZE 240U
#define PLAYER_RADIUS 10U
#define GAME_BASE_BACKGROUND_COLOUR 0x0255U /* GC9A01A_COLOR565(252, 248, 244) */
#define GAME_PLAYER_COLOUR GREEN
#define GAME_MPU_I2C_ADDR 0x68U

#define GAME_GYRO_SCALE 65.5F
#define GAME_GYRO_DEADZONE 2.0F

static world_t s_world;
static player_t s_player;
static mpu6050_handle_t s_mpu;

static uint16_t s_prev_draw_x;
static uint16_t s_prev_draw_y;
static uint8_t s_first_frame = 1U;
static uint32_t s_rng_state = 0x13572468UL;

static float game_map_gyro_to_force(int16_t gyro_raw)
{
    float dps;

    dps = ((float)gyro_raw) / GAME_GYRO_SCALE;

    if ((dps > (-GAME_GYRO_DEADZONE)) && (dps < GAME_GYRO_DEADZONE))
    {
        dps = 0.0F;
    }

    return dps;
}

static uint32_t game_rand_u32(void)
{
    s_rng_state = (1103515245UL * s_rng_state) + 12345UL;
    return s_rng_state;
}

static uint16_t game_rand_range(uint16_t min_value, uint16_t max_value)
{
    uint32_t span;
    uint32_t random_value;

    if (max_value <= min_value)
    {
        return min_value;
    }

    span = (uint32_t)max_value - (uint32_t)min_value + 1UL;
    random_value = game_rand_u32() % span;

    return (uint16_t)((uint32_t)min_value + random_value);
}

static uint16_t game_rand_colour(void)
{
    static const uint16_t colours[] = {RED,
                                       ORANGE,
                                       MAGENTA,
                                       VIOLET,
                                       INDIGO,
                                       BLUE,
                                       CYAN,
                                       GREEN,
                                       GREENYELLOW,
                                       PINK,
                                       PURPLE,
                                       GC9A01A_COLOR565(255, 120, 170),
                                       GC9A01A_COLOR565(120, 190, 255),
                                       GC9A01A_COLOR565(255, 160, 80),
                                       GC9A01A_COLOR565(120, 255, 180),
                                       GC9A01A_COLOR565(255, 110, 110)};

    return colours[game_rand_u32() % (sizeof(colours) / sizeof(colours[0]))];
}

static uint16_t game_get_player_draw_x(void)
{
    int32_t x;

    x = (int32_t)s_player.x - ((int32_t)BALL_IMG_W / 2L);

    if (x < 0L)
    {
        x = 0L;
    }

    if ((x + (int32_t)BALL_IMG_W) > (int32_t)LCD_SIZE)
    {
        x = (int32_t)LCD_SIZE - (int32_t)BALL_IMG_W;
    }

    return (uint16_t)x;
}

static uint16_t game_get_player_draw_y(void)
{
    int32_t y;

    y = (int32_t)s_player.y - ((int32_t)BALL_IMG_H / 2L);

    if (y < 0L)
    {
        y = 0L;
    }

    if ((y + (int32_t)BALL_IMG_H) > (int32_t)LCD_SIZE)
    {
        y = (int32_t)LCD_SIZE - (int32_t)BALL_IMG_H;
    }

    return (uint16_t)y;
}

static uint8_t game_rect_overlap(uint16_t rect1_x, uint16_t rect1_y, uint16_t rect1_w,
                                 uint16_t rect1_h, uint16_t rect2_x, uint16_t rect2_y,
                                 uint16_t rect2_w, uint16_t rect2_h)
{
    if ((uint32_t)rect1_x + (uint32_t)rect1_w <= (uint32_t)rect2_x)
    {
        return 0U;
    }

    if ((uint32_t)rect2_x + (uint32_t)rect2_w <= (uint32_t)rect1_x)
    {
        return 0U;
    }

    if ((uint32_t)rect1_y + (uint32_t)rect1_h <= (uint32_t)rect2_y)
    {
        return 0U;
    }

    if ((uint32_t)rect2_y + (uint32_t)rect2_h <= (uint32_t)rect1_y)
    {
        return 0U;
    }

    return 1U;
}

static void game_draw_background(void)
{
    gc9a01a_fill_screen(GAME_BASE_BACKGROUND_COLOUR);

    gc9a01a_fill_circle(15U, 20U, 70U, GC9A01A_COLOR565(255, 214, 230));
    gc9a01a_fill_circle(95U, 18U, 42U, GC9A01A_COLOR565(215, 232, 255));
    gc9a01a_fill_circle(185U, 22U, 58U, GC9A01A_COLOR565(222, 213, 255));
    gc9a01a_fill_circle(232U, 40U, 55U, GC9A01A_COLOR565(255, 228, 196));

    gc9a01a_fill_circle(28U, 110U, 48U, GC9A01A_COLOR565(255, 236, 170));
    gc9a01a_fill_circle(108U, 90U, 65U, GC9A01A_COLOR565(205, 246, 224));
    gc9a01a_fill_circle(190U, 115U, 52U, GC9A01A_COLOR565(255, 214, 214));
    gc9a01a_fill_circle(232U, 120U, 40U, GC9A01A_COLOR565(210, 240, 255));

    gc9a01a_fill_circle(22U, 208U, 55U, GC9A01A_COLOR565(220, 220, 255));
    gc9a01a_fill_circle(95U, 208U, 46U, GC9A01A_COLOR565(255, 224, 245));
    gc9a01a_fill_circle(170U, 210U, 60U, GC9A01A_COLOR565(220, 255, 210));
    gc9a01a_fill_circle(232U, 220U, 48U, GC9A01A_COLOR565(255, 230, 205));

    gc9a01a_fill_circle(52U, 42U, 20U, GC9A01A_COLOR565(255, 120, 170));
    gc9a01a_fill_circle(135U, 40U, 18U, GC9A01A_COLOR565(120, 190, 255));
    gc9a01a_fill_circle(205U, 58U, 16U, GC9A01A_COLOR565(180, 120, 255));

    gc9a01a_fill_circle(60U, 102U, 14U, GC9A01A_COLOR565(255, 160, 80));
    gc9a01a_fill_circle(132U, 112U, 22U, GC9A01A_COLOR565(120, 255, 180));
    gc9a01a_fill_circle(208U, 98U, 18U, GC9A01A_COLOR565(255, 110, 110));

    gc9a01a_fill_circle(38U, 180U, 16U, GC9A01A_COLOR565(95, 170, 255));
    gc9a01a_fill_circle(118U, 180U, 18U, GC9A01A_COLOR565(255, 110, 210));
    gc9a01a_fill_circle(198U, 182U, 22U, GC9A01A_COLOR565(120, 235, 120));

    gc9a01a_fill_circle(18U, 12U, 5U, MAGENTA);
    gc9a01a_fill_circle(32U, 18U, 7U, RED);
    gc9a01a_fill_circle(48U, 10U, 4U, ORANGE);
    gc9a01a_fill_circle(66U, 22U, 6U, VIOLET);
    gc9a01a_fill_circle(82U, 14U, 5U, INDIGO);
    gc9a01a_fill_circle(110U, 16U, 7U, CYAN);
    gc9a01a_fill_circle(126U, 10U, 4U, BLUE);
    gc9a01a_fill_circle(145U, 20U, 5U, PINK);
    gc9a01a_fill_circle(164U, 12U, 6U, GREENYELLOW);
    gc9a01a_fill_circle(182U, 18U, 4U, PURPLE);
    gc9a01a_fill_circle(205U, 16U, 6U, RED);
    gc9a01a_fill_circle(225U, 18U, 5U, ORANGE);

    gc9a01a_fill_circle(12U, 122U, 5U, RED);
    gc9a01a_fill_circle(24U, 138U, 7U, MAGENTA);
    gc9a01a_fill_circle(40U, 128U, 4U, ORANGE);
    gc9a01a_fill_circle(55U, 145U, 6U, BLUE);
    gc9a01a_fill_circle(74U, 132U, 5U, VIOLET);
    gc9a01a_fill_circle(92U, 148U, 7U, INDIGO);
    gc9a01a_fill_circle(110U, 132U, 4U, CYAN);
    gc9a01a_fill_circle(126U, 146U, 6U, GREEN);
    gc9a01a_fill_circle(146U, 130U, 5U, PINK);
    gc9a01a_fill_circle(164U, 146U, 7U, PURPLE);
    gc9a01a_fill_circle(182U, 132U, 4U, ORANGE);
    gc9a01a_fill_circle(198U, 146U, 6U, RED);
    gc9a01a_fill_circle(216U, 130U, 5U, MAGENTA);
    gc9a01a_fill_circle(230U, 144U, 4U, BLUE);
}

static void game_draw_random_paint(uint16_t ball_x, uint16_t ball_y)
{
    uint8_t count;
    uint8_t i;
    uint16_t x;
    uint16_t y;
    uint16_t r;
    uint16_t colour;
    uint16_t rx;
    uint16_t ry;
    uint16_t rw;
    uint16_t rh;

    if ((game_rand_u32() % 100U) > 40U)
    {
        return;
    }

    count = (uint8_t)game_rand_range(1U, 3U);

    for (i = 0U; i < count; i++)
    {
        r = game_rand_range(2U, 8U);

        x = game_rand_range(18U, LCD_SIZE);
        y = game_rand_range(18U, LCD_SIZE);

        if (x < r)
        {
            x = r;
        }

        if (y < r)
        {
            y = r;
        }

        if (((uint32_t)x + (uint32_t)r) >= (uint32_t)LCD_SIZE)
        {
            x = (uint16_t)((uint32_t)LCD_SIZE - (uint32_t)r - 1UL);
        }

        if (((uint32_t)y + (uint32_t)r) >= (uint32_t)LCD_SIZE)
        {
            y = (uint16_t)((uint32_t)LCD_SIZE - (uint32_t)r - 1UL);
        }

        rx = (uint16_t)((uint32_t)x - (uint32_t)r);
        ry = (uint16_t)((uint32_t)y - (uint32_t)r);
        rw = (uint16_t)((2UL * (uint32_t)r) + 1UL);
        rh = (uint16_t)((2UL * (uint32_t)r) + 1UL);

        if (game_rect_overlap(rx, ry, rw, rh, ball_x, ball_y, BALL_IMG_W, BALL_IMG_H) != 0U)
        {
            continue;
        }

        colour = game_rand_colour();
        gc9a01a_fill_circle(x, y, r, colour);
    }
}

err_t game_init(void)
{
    err_t status;
    uint16_t draw_x;
    uint16_t draw_y;

    bsp_lcd_init();

    world_init(&s_world, LCD_SIZE, LCD_SIZE, GAME_BASE_BACKGROUND_COLOUR);

    status = player_init(&s_player, s_world.center_x, s_world.center_y, PLAYER_RADIUS,
                         GAME_PLAYER_COLOUR);
    if (status != ERR_OK)
    {
        return status;
    }

    s_mpu = mpu6050_create(GAME_MPU_I2C_ADDR);
    if (s_mpu == 0)
    {
        return ERR_HW_FAILURE;
    }

    status = mpu6050_init(s_mpu);
    if (status != ERR_OK)
    {
        return status;
    }

    status = mpu6050_calibrate(s_mpu);
    if (status != ERR_OK)
    {
        return status;
    }

    game_draw_background();

    draw_x = game_get_player_draw_x();
    draw_y = game_get_player_draw_y();

    gc9a01a_draw_image(draw_x, BALL_IMG_W, draw_y, BALL_IMG_H, ball_1);

    s_prev_draw_x = draw_x;
    s_prev_draw_y = draw_y;
    s_first_frame = 0U;

    return ERR_OK;
}

err_t game_update(float dt_s)
{
    err_t status;
    mpu6050_gyro_sample_t sample;
    float force_x;
    float force_y;

    status = mpu6050_read_gyro(s_mpu, &sample);
    if (status != ERR_OK)
    {
        return status;
    }

    force_x = game_map_gyro_to_force(sample.gyro_y);
    force_y = game_map_gyro_to_force(sample.gyro_x);

    status = player_update(&s_player, force_x, force_y, dt_s);
    if (status != ERR_OK)
    {
        return status;
    }

    status =
        player_bounce_in_round_world(&s_player, s_world.center_x, s_world.center_y, s_world.radius);
    if (status != ERR_OK)
    {
        return status;
    }

    return ERR_OK;
}

err_t game_render(void)
{
    uint16_t draw_x;
    uint16_t draw_y;

    draw_x = game_get_player_draw_x();
    draw_y = game_get_player_draw_y();

    if ((draw_x == s_prev_draw_x) && (draw_y == s_prev_draw_y) && (s_first_frame == 0U))
    {
        game_draw_random_paint(draw_x, draw_y);
        return ERR_OK;
    }

    if (s_first_frame == 0U)
    {
        gc9a01a_fill_rect(s_prev_draw_x, BALL_IMG_W, s_prev_draw_y, BALL_IMG_H,
                          s_world.background_colour);
    }

    game_draw_random_paint(draw_x, draw_y);
    gc9a01a_draw_image(draw_x, BALL_IMG_W, draw_y, BALL_IMG_H, ball_1);

    s_prev_draw_x = draw_x;
    s_prev_draw_y = draw_y;
    s_first_frame = 0U;

    return ERR_OK;
}