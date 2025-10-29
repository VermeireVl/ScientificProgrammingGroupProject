# Slider properties
slider_x = screenParam[0] * 0.1
slider_y = screenParam[1] * 0.9
slider_width = screenParam[0] * 0.4
slider_height = screenParam[1] * 0.05
handle_radius = screenParam[1] * 0.025
slider_min_value = 0
slider_max_value = 100
slider_value = 50  # Initial value

# Calculate handle position
handle_x = slider_x + (slider_value / slider_max_value) * slider_width



elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse is on the handle
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if (slider_x <= mouse_x <= slider_x + slider_width and
                slider_y - handle_radius <= mouse_y <= slider_y + handle_radius):
                dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION and dragging:
            # Update handle position
            mouse_x, _ = pygame.mouse.get_pos()
            handle_x = max(slider_x, min(mouse_x, slider_x + slider_width))
            # Update slider value
            slider_value = ((handle_x - slider_x) / slider_width) * slider_max_value
