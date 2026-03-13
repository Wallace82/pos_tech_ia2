# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 10:54:21 2026

@author: paulo.goncalves
"""
import pygame
from pontos import ServicePoint
from draw_functions1 import draw_plot_panel

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (220, 220, 220)
DARK_GRAY = (120, 120, 120)
RED = (220, 50, 50)
ORANGE = (255, 140, 0)
BLUE = (50, 90, 220)
GREEN = (40, 170, 90)
PURPLE = (140, 70, 180)


def get_priority_color(priority: int) -> tuple[int, int, int]:
    if priority == 4:
        return RED
    if priority == 3:
        return ORANGE
    if priority == 2:
        return BLUE
    return GREEN


def draw_route_lines(screen: pygame.Surface, points: list[ServicePoint]) -> None:
    if len(points) < 2:
        return

    for i in range(len(points) - 1):
        start = points[i].posicao()
        end = points[i + 1].posicao()
        pygame.draw.line(screen, PURPLE, start, end, 2)


def draw_service_points(screen: pygame.Surface, points: list[ServicePoint], font: pygame.font.Font) -> None:
    for point in points:
        color = get_priority_color(point.prioridade)
        pygame.draw.circle(screen, color, point.posicao(), 7)
        label = font.render(str(point.id), True, BLACK)
        screen.blit(label, (point.x + 8, point.y - 8))


def draw_colored_bullet(
    screen: pygame.Surface,
    x: int,
    y: int,
    color: tuple[int, int, int],
    radius: int = 5
) -> None:
    pygame.draw.circle(screen, color, (x, y), radius)
    
def draw_scrollbar(
    screen: pygame.Surface,
    x: int,
    y: int,
    width: int,
    height: int,
    content_height: int,
    scroll_offset: int
) -> None:
    if content_height <= height:
        return
    
    pygame.draw.rect(screen, (210, 210, 210), (x, y, width, height))

    thumb_height = max(30, int(height * (height / content_height)))
    max_scroll = content_height - height
    thumb_y = y + int((scroll_offset / max_scroll) * (height - thumb_height))

    pygame.draw.rect(screen, DARK_GRAY, (x, thumb_y, width, thumb_height))
    
    
def draw_side_panel(
    screen: pygame.Surface,
    panel_x: int,
    panel_width: int,
    window_height: int,
    title_font: pygame.font.Font,
    text_font: pygame.font.Font,
    route: list[ServicePoint],
    generation: int,
    best_fitness: float,
    fitness_history: list[float],
    scroll_offset: int
) -> int:
    pygame.draw.rect(screen, GRAY, (panel_x, 0, panel_width, window_height))
    
    chart_height = 190

    draw_plot_panel(
        screen=screen,
        fitness_history=fitness_history,
        x=panel_x + 10,
        y=10,
        width=panel_width - 20,
        height=chart_height,
        x_label="Generation",
        y_label="Fitness"
    )
    
    content_x = panel_x + 16
    content_y = chart_height + 18

    title = title_font.render("Rota em tempo real", True, BLACK)
    screen.blit(title, (content_x, content_y))

    info_lines = [
        f"Geração: {generation}",
        f"Melhor fitness: {best_fitness:.2f}",
        ""
    ]
    
    y = content_y + 34
    for line in info_lines:
        text_surface = text_font.render(line, True, BLACK)
        screen.blit(text_surface, (content_x, y))
        y += 18

    # LEGENDA COM CORES
    LEGENDAS = [
        (4, "4 = Emergência obstétrica"),
        (3, "3 = Violência doméstica"),
        (2, "2 = Medicamento hormonal"),
        (1, "1 = Pós-parto"),
    ]

    legend_title = text_font.render("Prioridades:", True, BLACK)
    screen.blit(legend_title, (content_x, y))
    y += 22

    for priority, text_line in LEGENDAS:
        color = get_priority_color(priority)
        draw_colored_bullet(screen, content_x + 6, y + 6, color, radius=5)

        text_surface = text_font.render(text_line, True, BLACK)
        screen.blit(text_surface, (content_x + 20, y))
        y += 18

    y += 10
    
    route_title = text_font.render("Melhor rota atual:", True, BLACK)
    screen.blit(route_title, (content_x, y))
    y += 22
    
    route_start_y = y

    TIPOS_ATENDIMENTOS = {
        "Emergência obstétrica": "Emerg. obstétrica",
        "Violência doméstica": "Viol. doméstica",
        "Medicamento hormonal": "Med. hormonal",
        "Pós-parto": "Pós-parto",
    }

    line_height = 17
    column_width = (panel_width - 50) // 2
    col1_x = 0
    col2_x = column_width
    
    visible_area_height = window_height - route_start_y - 20
    items_per_column = visible_area_height // line_height
    if items_per_column < 1:
        items_per_column = 1
        
    total_items = len(route)
    total_rows = (total_items + 1) // 2 if total_items > items_per_column else total_items
    content_height = max(visible_area_height, total_rows * line_height)
    
    route_surface_width = panel_width - 40
    route_surface_height = content_height
    route_surface = pygame.Surface((route_surface_width, route_surface_height), pygame.SRCALPHA)
    route_surface.fill((0, 0, 0, 0))
    
    # LISTA DA ROTA COM BOLINHA DA MESMA COR DO MAPA
    for idx, point in enumerate(route, start=1):
        tipo = TIPOS_ATENDIMENTOS.get(point.tipo_atendimento, point.tipo_atendimento)
        color = get_priority_color(point.prioridade)

        text  = (
            f"{idx}. P{point.id} {point.codigo} | "
            f"{tipo} | D:{point.quantidade} | T:{point.tempo_atendimento:.1f}h"
        )
        
        if idx <= items_per_column:
            draw_x = col1_x
            draw_y = (idx - 1) * line_height
        else:
            draw_x = col2_x
            draw_y = (idx - items_per_column - 1) * line_height
        
        draw_colored_bullet(route_surface, draw_x + 6, draw_y + 6, color, radius=5)
        line_surface = text_font.render(text, True, BLACK)
        route_surface.blit(line_surface, (draw_x + 18, draw_y))
        
    clip_rect = pygame.Rect(0, scroll_offset, route_surface_width, visible_area_height)
    screen.blit(route_surface, (content_x, route_start_y), clip_rect)

    scrollbar_x = panel_x + panel_width - 14
    draw_scrollbar(
        screen=screen,
        x=scrollbar_x,
        y=route_start_y,
        width=8,
        height=visible_area_height,
        content_height=route_surface_height,
        scroll_offset=scroll_offset
    )

    max_scroll = max(0, route_surface_height - visible_area_height)
    return max_scroll