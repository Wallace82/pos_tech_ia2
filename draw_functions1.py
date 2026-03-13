# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 16:56:23 2026

@author: paulo
"""

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
import pygame


def draw_plot_panel(
    screen: pygame.Surface,
    fitness_history: list[float],
    x: int,
    y: int,
    width: int,
    height: int,
    x_label: str = "Generation",
    y_label: str = "Fitness"
) -> None:
    """
    Desenha um gráfico de evolução do fitness usando Matplotlib
    e o renderiza dentro da tela do Pygame.
    """

    if not fitness_history:
        return

    generations = list(range(len(fitness_history)))

    dpi = 100
    fig_width = width / dpi
    fig_height = height / dpi

    fig, ax = plt.subplots(figsize=(fig_width, fig_height), dpi=dpi)

    ax.plot(generations, fitness_history, linewidth=1.8)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    ax.grid(False)
    fig.tight_layout()

    canvas = FigureCanvasAgg(fig)
    canvas.draw()
    renderer = canvas.get_renderer()
    raw_data = renderer.buffer_rgba()

    size = canvas.get_width_height()
    surf = pygame.image.frombuffer(raw_data, size, "RGBA")
    screen.blit(surf, (x, y))

    plt.close(fig)