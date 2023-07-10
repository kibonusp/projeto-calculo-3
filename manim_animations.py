from manim import *

def axis_vector_field(scene: Scene, func: np.array, wait_time: int = 5):
        numberplane = NumberPlane()
        array_field = ArrowVectorField(func)

        scene.play(FadeIn(array_field), FadeIn(numberplane))

        stream_lines = StreamLines(
            func, 
            stroke_width=1,
            max_anchors_per_line=10,
            # stroke_width=3, max_anchors_per_line=5, virtual_time=1
        )

        scene.add(stream_lines)
        stream_lines.start_animation(warm_up=True, flow_speed=1, time_width=0.5)
        scene.wait(wait_time)
        # scene.play(stream_lines.end_animation())
        scene.remove(stream_lines, numberplane, array_field)
   


class Axes3DExplanation(ThreeDScene):
    def construct(self):
        title = Text('Universo 2D?')
        self.play(FadeIn(title))
        self.wait(2)
        self.play(FadeOut(title))

        axes = ThreeDAxes()

        x_label = axes.get_x_axis_label(Tex("x"))
        y_label = axes.get_y_axis_label(Tex("y")).shift(UP * 1.8)

        # zoom out so we see the axes
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)

        self.play(FadeIn(axes), FadeIn(x_label), FadeIn(y_label))

        self.wait(0.5)

        # built-in updater which begins camera rotation
        self.begin_ambient_camera_rotation(rate=0.15)
        
        sphere = Sphere(radius=2, resolution=(18, 18))
        cylinder = Cylinder(radius=2, height=0.1)

        self.wait(8)

        self.play(FadeIn(sphere))

        self.wait(2)

        # animate the move of the camera to properly see the axes
        self.move_camera(phi=0 * DEGREES, theta=270 * DEGREES, zoom=0.5, run_time=1.5)
        
        self.stop_ambient_camera_rotation()
        
        self.play(FadeTransform(sphere, cylinder))

        self.wait(4)


class VectorFieldScene(Scene):
    def construct(self):
        f1 = lambda pos: np.array([np.sin(pos[0]), pos[1] ** 2, 0])
        f2 = lambda pos: np.array([-(pos[1]), pos[0], 0])
        ftex = MathTex(r"F(x,y)").move_to(3 * RIGHT + 2.3 * UP)
        f1tex = MathTex(r"F(x,y)=(\sin x, y^{2})").move_to(3 * RIGHT + 2.3 * UP)
        f2tex = MathTex(r"F(x,y)=(-y, x)").move_to(3 * RIGHT + 2.3 * UP)

        numberplane = NumberPlane()
        self.play(FadeIn(numberplane), FadeIn(ftex))

        self.wait(2)
        array_field1 = ArrowVectorField(f1)

        self.play(Transform(ftex, f1tex))
        self.wait(2)
        self.play(FadeIn(array_field1))
        self.bring_to_back(array_field1)


        self.wait(3)
        array_field2 = ArrowVectorField(f2)
        # self.remove(array_field1)
        self.play(FadeTransform(array_field1, array_field2), FadeTransform(ftex, f2tex))
        # self.bring_to_back(array_field2)

        self.wait(3)

        self.remove(numberplane, array_field2, f2tex)



class Divergence(Scene):
    def construct(self):
        title = Text('Divergente')
        self.play(FadeIn(title))
        self.wait(4)
        self.play(FadeOut(title))

        # self.wait(3)
        positive_div = MathTex(r"\text{div} > 0")
        positive_tex = MathTex(r"F(x, y) = (x, y)").next_to(positive_div, DOWN)
        positive_group = VGroup(positive_div, positive_tex)
        self.play(Write(positive_group))
        self.wait(2)
        self.play(FadeOut(positive_group))

        positive_func = lambda pos: np.array([pos[0], pos[1], 0])
        axis_vector_field(self, positive_func)

        negative_div = MathTex(r"\text{div} < 0")
        negative_tex = MathTex(r"F(x, y) = (-x, -y)").next_to(negative_div, DOWN)
        negative_group = VGroup(negative_div, negative_tex)
        self.play(Write(negative_group))
        self.wait(2)
        self.play(FadeOut(negative_group))

        negative_func = lambda pos: np.array([-pos[0], -pos[1], 0])
        axis_vector_field(self, negative_func)


class Mountain(ThreeDScene):
    def construct(self):
        title = Text('Gradiente')
        self.play(FadeIn(title))
        self.wait(2)
        self.play(FadeOut(title))

        resolution_fa = 8
        self.set_camera_orientation(phi=75 * DEGREES, theta=-160 * DEGREES)
        self.move_camera(zoom=0.8, run_time=1.5)
        axes = ThreeDAxes(x_range=(0, 5, 1), y_range=(0, 5, 1), z_range=(-1, 1, 0.5))
        def param_surface(u, v):
            x = u
            y = v
            z = np.sin(x) * np.cos(y)
            return z
        surface_plane = Surface(
            lambda u, v: axes.c2p(u, v, param_surface(u, v)),
            resolution=(resolution_fa, resolution_fa),
            v_range=[0, 5],
            u_range=[0, 5],
            )
        surface_plane.set_style(fill_opacity=1)
        surface_plane.set_fill_by_value(axes=axes, colorscale=[(GREEN_A, -0.5), (GREEN_B, 0), (GREEN_C, 0.5)], axis=2)
        self.wait(2)
        self.play(FadeIn(surface_plane))
        self.begin_ambient_camera_rotation(rate=0.15)

        self.wait(21)
        self.play(FadeOut(surface_plane))

class Gradiente(Scene):
    def construct(self):
        grad = MathTex(r"\nabla = (\frac{\partial }{\partial x}, \frac{\partial }{\partial y})")
        self.play(Write(grad))
        self.wait(2)
        self.play(FadeOut(grad))

        grad_div = MathTex(r"\text{div} F = \nabla \cdot F")
        self.play(Write(grad_div))
        self.wait(2)
        self.play(FadeOut(grad_div))


class NavierStokes(Scene):
    def construct(self):
        title = Text('Equações de fluidos incompressíveis')
        self.play(FadeIn(title))
        self.wait(2)
        self.play(FadeOut(title))

        t1 = MathTex(r"u: \text{ Campo de velocidade}")
        t2 = MathTex(r"p: \text{ Campo de pressão}")
        t3 = MathTex(r"t: \text{ Tempo}")
        t4 = MathTex(r"\nu: \text{ Viscosidade}")
        t5 = MathTex(r"\rho: \text{ Densidade do fluido}")
        t6 = MathTex(r"f: \text{ Forças externas}")
        x = VGroup(t1, t2, t3, t4, t5, t6).arrange(direction=DOWN, aligned_edge=LEFT).scale(0.7)
        x.set_opacity(0.5)
        self.play(FadeIn(x))

        self.wait()
        t1.set_opacity(1)

        self.wait(3.5)
        t2.set_opacity(1)
        t1.set_opacity(0.5)

        self.wait(3)
        t3.set_opacity(1)
        t2.set_opacity(0.5)

        self.wait(2)
        t4.set_opacity(1)
        t3.set_opacity(0.5)

        self.wait(3)
        t5.set_opacity(1)
        t4.set_opacity(0.5)

        self.wait(2)
        t6.set_opacity(1)
        t5.set_opacity(0.5)

        self.wait(3)
        t6.set_opacity(0.5)
        self.wait()
        self.play(FadeOut(x))


        ns_equation = MathTex(r"\frac{\partial u}{\partial t}", "=", 
            r"-(u \cdot \nabla)u", "-", r"\frac{1}{\rho}\nabla p", "+", r"\nu \nabla ^ 2 u", 
            "+", "f")
        div0 = MathTex(r"\nabla \cdot u = 0")

        ut_box = SurroundingRectangle(ns_equation[0], buff = .1)
        div_box = SurroundingRectangle(ns_equation[2], buff = .1)
        in_force_box = SurroundingRectangle(ns_equation[4], buff = .1)
        diff_box = SurroundingRectangle(ns_equation[6], buff = .1)
        ex_force_box = SurroundingRectangle(ns_equation[8], buff = .1)
        
        both_eq = VGroup(ns_equation.shift(UP), div0.shift(DOWN))

        self.play(Write(both_eq))
        self.wait(2)
        self.play(FadeOut(both_eq))

        self.play(Write(div0.shift(UP)))
        self.wait(6)
        self.play(FadeOut(div0))


        self.play(Write(ns_equation.shift(DOWN)))
        self.wait(12)
        self.play(Create(ut_box))
        self.wait(4)
        self.play(ReplacementTransform(ut_box, div_box))
        self.wait(3.5)
        self.play(ReplacementTransform(div_box, in_force_box))
        self.wait(5)
        self.play(ReplacementTransform(in_force_box, diff_box))
        self.wait(4)
        self.play(ReplacementTransform(diff_box, ex_force_box))
        self.wait(2)
        self.play(FadeOut(ex_force_box))


class ContinuousMotion(Scene):
    def construct(self):
        func = lambda pos: np.sin(pos[0] / 2) * UR + np.cos(pos[1] / 2) * LEFT
        stream_lines = StreamLines(func, stroke_width=3, max_anchors_per_line=30)
        self.add(stream_lines)
        stream_lines.start_animation(warm_up=False, flow_speed=1.5)
        self.wait(stream_lines.virtual_time / stream_lines.flow_speed)
        

class Presentation(Scene):
    def construct(self):
        trab = Text("Trabalho de Cálculo 3").to_edge(UP).scale(0.75)
        title = Text("Simulação Visual de Mecânica de Fluidos")
        subtitle = Text("Bacharelado em Ciências da Computação").next_to(title, DOWN).scale(0.5)

        self.play(Write(trab))
        self.play(Write(title), Write(subtitle))

        self.wait(2)

        self.play(FadeOut(title), FadeOut(subtitle))

        members = Paragraph(
            "Davi Fagundes\n"
            "Gabriel Freitas\n"
            "Gustavo Sampaio\n"
            "Thaís Ribeiro\n"
            "Théo Riffel\n"
            "Vítor Fróis").scale(0.7)

        self.play(FadeIn(members))
        self.wait(6)
        self.play(FadeOut(members), FadeOut(trab))

class References(Scene):
    def construct(self):
        title = Text("Referências")
        self.play(FadeIn(title))
        self.wait(2)
        self.play(FadeOut(title))

        ref = Paragraph(
            "Divergence and curl - 3Blue1Brown\n"
            "Stable Fluids implemented in Python/NumPy - Machine Learning & Simulation\n"
            "Stable Fluids - Jos Stam").scale(0.5).to_edge(LEFT)

        self.play(FadeIn(ref))
        self.wait(3)


        func = lambda pos: np.sin(pos[0] / 3) * DOWN + np.cos(pos[1] / 2) * RIGHT
        stream_lines = StreamLines(func, stroke_width=3, max_anchors_per_line=30)
        self.add(stream_lines)
        stream_lines.start_animation(warm_up=True, flow_speed=1.5)
        self.play(FadeOut(ref, run_time=3))
        self.wait(5)
        self.play(stream_lines.end_animation())
        
class TitleVideo(Scene):
    def construct(self):
        title_str = input("Insira título do vídeo: ")
        title = Text(title_str)
        self.play(FadeIn(title))
        self.wait(2)
        self.play(FadeOut(title))




