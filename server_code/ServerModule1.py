import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json
import random

# ─────────────────────────────────────────────────────────────────────────────
# QUESTIONS DATA
# All 120 questions: 4 topics × 3 difficulties × 10 questions each
# LaTeX strings preserved exactly from the React source
# ─────────────────────────────────────────────────────────────────────────────

QUESTIONS = {
    "Differentiation": {
        "Easy": [
            {"id": 1, "question": "What is the derivative of $x^2$?", "options": ["$x$", "$2x$", "$2x^2$", "$x^2$"], "correctIndex": 1},
            {"id": 2, "question": "What is the derivative of $5x^3$?", "options": ["$5x^2$", "$15x^2$", "$15x^3$", "$3x^2$"], "correctIndex": 1},
            {"id": 3, "question": r"What is $\frac{d}{dx}(\sin x)$?", "options": [r"$\cos x$", r"$-\cos x$", r"$-\sin x$", r"$\tan x$"], "correctIndex": 0},
            {"id": 4, "question": r"What is $\frac{d}{dx}(e^x)$?", "options": [r"$xe^{x-1}$", r"$e^x$", r"$e^{x-1}$", r"$\ln x$"], "correctIndex": 1},
            {"id": 5, "question": "What is the derivative of a constant?", "options": ["$1$", "$0$", "The constant itself", "Undefined"], "correctIndex": 1},
            {"id": 6, "question": r"What is $\frac{d}{dx}(\ln x)$?", "options": [r"$e^x$", r"$\frac{1}{x^2}$", r"$\frac{1}{x}$", r"$x$"], "correctIndex": 2},
            {"id": 7, "question": r"What is the derivative of $\cos x$?", "options": [r"$\sin x$", r"$-\sin x$", r"$\cos x$", r"$-\cos x$"], "correctIndex": 1},
            {"id": 8, "question": r"What is $\frac{d}{dx}(x^4)$?", "options": [r"$x^3$", r"$4x^3$", r"$4x^4$", r"$3x^3$"], "correctIndex": 1},
            {"id": 9, "question": "What is the gradient of $y = 3x + 7$?", "options": ["$7$", "$3x$", "$3$", "$10$"], "correctIndex": 2},
            {"id": 10, "question": r"What is $\frac{d}{dx}(x)$?", "options": ["$0$", "$x$", "$1$", "$x^2$"], "correctIndex": 2},
        ],
        "Medium": [
            {"id": 1, "question": r"Find $\frac{dy}{dx}$ for $y = x^3 - 4x^2 + 2x$", "options": [r"$3x^2 - 8x + 2$", r"$3x^2 - 4x$", r"$x^2 - 8x + 2$", r"$3x^2 - 8x$"], "correctIndex": 0},
            {"id": 2, "question": r"What is $\frac{d}{dx}(x \sin x)$?", "options": [r"$\cos x$", r"$x\cos x + \sin x$", r"$\sin x + x$", r"$x\cos x$"], "correctIndex": 1},
            {"id": 3, "question": r"What is the chain rule for $\frac{d}{dx}(f(g(x)))$?", "options": [r"$f'(x) \cdot g'(x)$", r"$f(g'(x))$", r"$f'(g(x)) \cdot g'(x)$", r"$f'(g(x))$"], "correctIndex": 2},
            {"id": 4, "question": r"What is $\frac{d}{dx}(e^{2x})$?", "options": [r"$2e^{2x}$", r"$e^{2x}$", r"$2e^x$", r"$e^{2x-1}$"], "correctIndex": 0},
            {"id": 5, "question": r"What is $\frac{d}{dx}(\sin(3x))$?", "options": [r"$\cos(3x)$", r"$3\cos(3x)$", r"$-\cos(3x)$", r"$3\sin(3x)$"], "correctIndex": 1},
            {"id": 6, "question": "Find the stationary point of $y = x^2 - 6x + 8$", "options": ["$x = 2$", "$x = 3$", "$x = 4$", "$x = 6$"], "correctIndex": 1},
            {"id": 7, "question": r"What is $\frac{d}{dx}(\ln(2x))$?", "options": [r"$\frac{1}{2x}$", r"$\frac{2}{x}$", r"$\frac{1}{x}$", r"$2\ln x$"], "correctIndex": 2},
            {"id": 8, "question": r"What is $\frac{d}{dx}\left(\frac{x}{\sin x}\right)$?", "options": [r"$\frac{\sin x - x\cos x}{\sin^2 x}$", r"$\frac{1}{\cos x}$", r"$\frac{\sin x + x\cos x}{\sin^2 x}$", r"$\frac{\cos x}{\sin^2 x}$"], "correctIndex": 0},
            {"id": 9, "question": r"What is $\frac{d}{dx}(\tan x)$?", "options": [r"$\sec x$", r"$\sec^2 x$", r"$-\sec^2 x$", r"$\csc x$"], "correctIndex": 1},
            {"id": 10, "question": "Which rule differentiates $f(x) \\cdot g(x)$?", "options": ["Chain rule", "Quotient rule", "Product rule", "Sum rule"], "correctIndex": 2},
        ],
        "Hard": [
            {"id": 1, "question": r"Find $\frac{d^2y}{dx^2}$ for $y = x^4 - 3x^2$", "options": [r"$4x^3 - 6x$", r"$12x^2 - 6$", r"$12x - 6$", r"$4x^2 - 3$"], "correctIndex": 1},
            {"id": 2, "question": r"What is $\frac{d}{dx}(\arcsin x)$?", "options": [r"$\frac{1}{\sqrt{1-x^2}}$", r"$\frac{-1}{\sqrt{1-x^2}}$", r"$\frac{1}{\sqrt{1+x^2}}$", r"$\arccos x$"], "correctIndex": 0},
            {"id": 3, "question": r"Differentiate implicitly: $x^2 + y^2 = 25$", "options": [r"$\frac{dy}{dx} = \frac{x}{y}$", r"$\frac{dy}{dx} = -\frac{x}{y}$", r"$\frac{dy}{dx} = \frac{y}{x}$", r"$\frac{dy}{dx} = -\frac{y}{x}$"], "correctIndex": 1},
            {"id": 4, "question": r"What is $\frac{d}{dx}(x^x)$?", "options": [r"$x^x$", r"$x^{x-1}$", r"$x^x(1 + \ln x)$", r"$x \cdot x^{x-1}$"], "correctIndex": 2},
            {"id": 5, "question": r"If $y = e^{x^2}$, find $\frac{dy}{dx}$", "options": [r"$e^{x^2}$", r"$2x e^{x^2}$", r"$x^2 e^{x^2-1}$", r"$2e^{x^2}$"], "correctIndex": 1},
            {"id": 6, "question": "What condition identifies a point of inflection?", "options": [r"$\frac{dy}{dx} = 0$", r"$\frac{d^2y}{dx^2} = 0$ and changes sign", r"$\frac{d^2y}{dx^2} > 0$", r"$\frac{dy}{dx}$ changes sign"], "correctIndex": 1},
            {"id": 7, "question": r"Find $\frac{d}{dx}(\arctan x)$", "options": [r"$\frac{1}{1+x^2}$", r"$\frac{-1}{1+x^2}$", r"$\frac{1}{1-x^2}$", r"$\frac{1}{\sqrt{1+x^2}}$"], "correctIndex": 0},
            {"id": 8, "question": r"Differentiate $y = \cos^2(x)$ using the chain rule", "options": [r"$2\cos x$", r"$-\sin(2x)$", r"$-2\cos x \sin x$", "Both B and C"], "correctIndex": 3},
            {"id": 9, "question": r"What is the derivative of $\sinh(x)$?", "options": [r"$\cosh x$", r"$-\cosh x$", r"$\tanh x$", r"$-\sinh x$"], "correctIndex": 0},
            {"id": 10, "question": r"If $f(x) = \ln(\cos x)$, find $f'(x)$", "options": [r"$\frac{1}{\cos x}$", r"$-\tan x$", r"$\tan x$", r"$\frac{-\sin x}{\cos^2 x}$"], "correctIndex": 1},
        ],
    },
    "Integration": {
        "Easy": [
            {"id": 1, "question": r"What is $\int x \, dx$?", "options": [r"$x^2$", r"$\frac{x^2}{2} + c$", r"$2x + c$", r"$x + c$"], "correctIndex": 1},
            {"id": 2, "question": r"What is $\int \cos x \, dx$?", "options": [r"$-\sin x + c$", r"$\sin x + c$", r"$-\cos x + c$", r"$\tan x + c$"], "correctIndex": 1},
            {"id": 3, "question": r"What is $\int e^x \, dx$?", "options": [r"$xe^x + c$", r"$e^{x+1} + c$", r"$e^x + c$", r"$\ln x + c$"], "correctIndex": 2},
            {"id": 4, "question": r"What is $\int \frac{1}{x} \, dx$?", "options": [r"$x + c$", r"$-\frac{1}{x^2} + c$", r"$\ln|x| + c$", r"$\frac{1}{x^2} + c$"], "correctIndex": 2},
            {"id": 5, "question": r"What is $\int 3x^2 \, dx$?", "options": [r"$6x + c$", r"$x^3 + c$", r"$3x^3 + c$", r"$x^2 + c$"], "correctIndex": 1},
            {"id": 6, "question": r"What is $\int \sin x \, dx$?", "options": [r"$\cos x + c$", r"$-\cos x + c$", r"$\sin x + c$", r"$-\sin x + c$"], "correctIndex": 1},
            {"id": 7, "question": "What is the constant of integration?", "options": ["$k$", "$a$", "$c$", "$b$"], "correctIndex": 2},
            {"id": 8, "question": r"What is $\int 5 \, dx$?", "options": ["$5$", "$5x$", r"$5x + c$", "$0$"], "correctIndex": 2},
            {"id": 9, "question": r"What is $\int x^3 \, dx$?", "options": [r"$3x^2 + c$", r"$\frac{x^4}{4} + c$", r"$x^4 + c$", r"$4x^3 + c$"], "correctIndex": 1},
            {"id": 10, "question": "Integration is the reverse of which operation?", "options": ["Multiplication", "Differentiation", "Division", "Substitution"], "correctIndex": 1},
        ],
        "Medium": [
            {"id": 1, "question": r"What is $\int (2x + 3)^5 \, dx$?", "options": [r"$\frac{(2x+3)^6}{6} + c$", r"$\frac{(2x+3)^6}{12} + c$", r"$5(2x+3)^4 + c$", r"$(2x+3)^6 + c$"], "correctIndex": 1},
            {"id": 2, "question": r"What is $\int_0^2 x^2 \, dx$?", "options": [r"$\frac{4}{3}$", r"$\frac{8}{3}$", "$4$", "$8$"], "correctIndex": 1},
            {"id": 3, "question": r"What is $\int x e^x \, dx$?", "options": [r"$xe^x + c$", r"$e^x(x-1) + c$", r"$e^x(x+1) + c$", r"$x^2 e^x + c$"], "correctIndex": 1},
            {"id": 4, "question": r"What is $\int \sin^2 x \, dx$?", "options": [r"$\frac{x}{2} - \frac{\sin 2x}{4} + c$", r"$\frac{x}{2} + \frac{\sin 2x}{4} + c$", r"$-\cos^2 x + c$", r"$\frac{\sin 2x}{2} + c$"], "correctIndex": 0},
            {"id": 5, "question": "What technique integrates $x \\cos x$?", "options": ["Substitution", "Partial fractions", "Integration by parts", "Chain rule"], "correctIndex": 2},
            {"id": 6, "question": r"What is $\int e^{3x} \, dx$?", "options": [r"$3e^{3x} + c$", r"$\frac{e^{3x}}{3} + c$", r"$e^{3x} + c$", r"$e^{3x-1} + c$"], "correctIndex": 1},
            {"id": 7, "question": r"What is $\int \frac{1}{1+x^2} \, dx$?", "options": [r"$\ln(1+x^2) + c$", r"$\arctan x + c$", r"$\arcsin x + c$", r"$\frac{1}{2x} + c$"], "correctIndex": 1},
            {"id": 8, "question": r"What is $\int \tan x \, dx$?", "options": [r"$\sec^2 x + c$", r"$\ln|\cos x| + c$", r"$-\ln|\cos x| + c$", r"$\ln|\sin x| + c$"], "correctIndex": 2},
            {"id": 9, "question": r"Evaluate $\int_1^3 (x^2 - 1) \, dx$", "options": [r"$\frac{16}{3}$", r"$\frac{20}{3}$", r"$\frac{8}{3}$", r"$\frac{14}{3}$"], "correctIndex": 1},
            {"id": 10, "question": r"What is $\int (3x^2 + 2x) \, dx$?", "options": [r"$x^3 + x^2$", r"$x^3 + x^2 + c$", r"$6x + 2 + c$", r"$x^2 + 2x + c$"], "correctIndex": 1},
        ],
        "Hard": [
            {"id": 1, "question": r"What is $\int x^2 \ln x \, dx$?", "options": [r"$\frac{x^3 \ln x}{3} - \frac{x^3}{9} + c$", r"$\frac{x^3 \ln x}{3} + \frac{x^3}{9} + c$", r"$\frac{x^3}{3} \ln x + c$", r"$\frac{x^2}{2 \ln x} + c$"], "correctIndex": 0},
            {"id": 2, "question": r"What is $\int \frac{1}{x^2-1} \, dx$?", "options": [r"$\frac{1}{2}\ln\left|\frac{x-1}{x+1}\right| + c$", r"$\frac{1}{2}\ln\left|\frac{x+1}{x-1}\right| + c$", r"$\arctan x + c$", r"$\ln|x^2-1| + c$"], "correctIndex": 0},
            {"id": 3, "question": r"Evaluate $\int_0^{\pi/2} \sin x \cos x \, dx$", "options": ["$0$", r"$\frac{1}{4}$", r"$\frac{1}{2}$", "$1$"], "correctIndex": 2},
            {"id": 4, "question": r"What is $\int \sqrt{1-x^2} \, dx$?", "options": [r"$\arcsin x + c$", r"$\frac{x\sqrt{1-x^2}}{2} + \frac{\arcsin x}{2} + c$", r"$-\arccos x + c$", r"$\frac{\sqrt{1-x^2}}{x} + c$"], "correctIndex": 1},
            {"id": 5, "question": r"What is $\int \sec^2 x \tan x \, dx$?", "options": [r"$\frac{\tan^2 x}{2} + c$", r"$\frac{\sec^2 x}{2} + c$", r"$\sec x + c$", "Both A and B"], "correctIndex": 3},
            {"id": 6, "question": r"Use substitution $u = x^2$ to find $\int 2x e^{x^2} \, dx$", "options": [r"$2xe^{x^2} + c$", r"$e^{x^2} + c$", r"$x^2 e^{x^2} + c$", r"$\frac{e^{x^2}}{x} + c$"], "correctIndex": 1},
            {"id": 7, "question": r"What is $\int \frac{1}{x(x+1)} \, dx$?", "options": [r"$\ln\left|\frac{x}{x+1}\right| + c$", r"$\ln\left|\frac{x+1}{x}\right| + c$", r"$\frac{1}{x} - \frac{1}{x+1} + c$", r"$\ln|x| - \ln|x+1| + c$"], "correctIndex": 0},
            {"id": 8, "question": "What is the formula for integration by parts?", "options": [r"$\int uv \, dx = uv - \int vu' \, dx$", r"$\int u v' \, dx = uv - \int u'v \, dx$", r"$\int u'v' \, dx = uv + c$", r"$\int uv \, dx = u'v + uv' + c$"], "correctIndex": 1},
            {"id": 9, "question": r"What is $\int \cos^3 x \, dx$?", "options": [r"$\sin x - \frac{\sin^3 x}{3} + c$", r"$3\cos^2 x \sin x + c$", r"$\frac{\sin^3 x}{3} + c$", r"$\sin x + \sin^3 x + c$"], "correctIndex": 0},
            {"id": 10, "question": r"What is $\int x^2 e^x \, dx$?", "options": [r"$e^x(x^2 - 2x + 2) + c$", r"$e^x(x^2 + 2x + 2) + c$", r"$x^2 e^x - 2xe^x + c$", r"$e^x(x^2 - 2) + c$"], "correctIndex": 0},
        ],
    },
    "Graphs": {
        "Easy": [
            {"id": 1, "question": "What shape is the graph of $y = x^2$?", "options": ["Circle", "Parabola", "Ellipse", "Hyperbola"], "correctIndex": 1},
            {"id": 2, "question": "Where does $y = x^2 + 3$ cross the $y$-axis?", "options": ["$(0, 0)$", "$(3, 0)$", "$(0, 3)$", "$(0, -3)$"], "correctIndex": 2},
            {"id": 3, "question": "What is the $y$-intercept of $y = 2x + 5$?", "options": ["$2$", "$5$", "$0$", "$-5$"], "correctIndex": 1},
            {"id": 4, "question": "What does $y = -x^2$ look like compared to $y = x^2$?", "options": ["Wider", "Narrower", "Reflected in $x$-axis", "Reflected in $y$-axis"], "correctIndex": 2},
            {"id": 5, "question": "What is the vertex of $y = (x-3)^2 + 1$?", "options": ["$(1, 3)$", "$(3, 1)$", "$(-3, 1)$", "$(3, -1)$"], "correctIndex": 1},
            {"id": 6, "question": "If $y = f(x)$, what does $y = f(x) + 2$ represent?", "options": ["Shift right 2", "Shift left 2", "Shift up 2", "Shift down 2"], "correctIndex": 2},
            {"id": 7, "question": "What is the gradient of a horizontal line?", "options": ["$1$", "Undefined", "$0$", "$-1$"], "correctIndex": 2},
            {"id": 8, "question": "Where does $y = x^2 - 4$ cross the $x$-axis?", "options": [r"$x = 2$ only", r"$x = \pm 4$", r"$x = \pm 2$", r"$x = 4$ only"], "correctIndex": 2},
            {"id": 9, "question": "What does $y = f(-x)$ represent?", "options": ["Reflection in $x$-axis", "Reflection in $y$-axis", "Stretch by factor 2", "Translation up"], "correctIndex": 1},
            {"id": 10, "question": "How many times does $y = x^2$ touch the $x$-axis?", "options": ["Never", "Once", "Twice", "Three times"], "correctIndex": 1},
        ],
        "Medium": [
            {"id": 1, "question": "The graph $y = f(2x)$ is which transformation of $y = f(x)$?", "options": [r"Stretch by $2$ in $x$-direction", r"Stretch by $\frac{1}{2}$ in $x$-direction", r"Stretch by $2$ in $y$-direction", r"Translation by $2$"], "correctIndex": 1},
            {"id": 2, "question": "Find the range of $y = x^2 - 4x + 5$", "options": [r"$y \geq 0$", r"$y \geq 1$", r"$y \geq 5$", r"$y \geq -4$"], "correctIndex": 1},
            {"id": 3, "question": r"What are the asymptotes of $y = \frac{1}{x-2}$?", "options": ["$x = 0$", "$x = 2$", "$y = 2$", "$y = 0$ and $x = 2$"], "correctIndex": 3},
            {"id": 4, "question": "If $f(x) = x^2 - 6x + 8$, what are the $x$-intercepts?", "options": ["$x = 2, x = 4$", "$x = -2, x = -4$", "$x = 2, x = -4$", "$x = 1, x = 8$"], "correctIndex": 0},
            {"id": 5, "question": "Which transformation of $y = f(x)$ gives $y = 2f(x)$?", "options": [r"Stretch by $2$ in $x$", r"Stretch by $\frac{1}{2}$ in $y$", r"Stretch by $2$ in $y$", r"Stretch by $\frac{1}{2}$ in $x$"], "correctIndex": 2},
            {"id": 6, "question": "What is the period of $y = \\sin(2x)$?", "options": [r"$2\pi$", r"$\pi$", r"$\frac{\pi}{2}$", r"$4\pi$"], "correctIndex": 1},
            {"id": 7, "question": "How do you find a turning point from a quadratic in completed square form?", "options": ["Read off the $x$-intercepts", "Read off the vertex directly", "Differentiate and set to $0$", "Find the $y$-intercept"], "correctIndex": 1},
            {"id": 8, "question": "What does $|m| > 1$ mean for the line $y = mx + c$?", "options": [r"Shallower than $45°$", r"Steeper than $45°$", "Negative gradient", "Parallel to $x$-axis"], "correctIndex": 1},
            {"id": 9, "question": "What is the inverse of $y = 2x + 1$?", "options": [r"$y = \frac{x-1}{2}$", r"$y = 2x - 1$", r"$y = \frac{x+1}{2}$", r"$y = \frac{1}{2x+1}$"], "correctIndex": 0},
            {"id": 10, "question": "What transformation takes $y = f(x)$ to $y = f(x-3)$?", "options": [r"Shift up $3$", r"Shift left $3$", r"Shift right $3$", r"Shift down $3$"], "correctIndex": 2},
        ],
        "Hard": [
            {"id": 1, "question": r"How many vertical asymptotes does $y = \frac{1}{x^2-1}$ have?", "options": ["$0$", "$1$", "$2$", "$3$"], "correctIndex": 2},
            {"id": 2, "question": "For $y = x^3 - 3x$, find the coordinates of the local maximum", "options": ["$(-1, 2)$", "$(1, -2)$", "$(-1, -2)$", "$(1, 2)$"], "correctIndex": 0},
            {"id": 3, "question": r"What is the range of $y = 3\sin(x) + 1$?", "options": [r"$-3 \leq y \leq 3$", r"$-2 \leq y \leq 4$", r"$1 \leq y \leq 4$", r"$0 \leq y \leq 4$"], "correctIndex": 1},
            {"id": 4, "question": "If $f$ is an odd function, what is $f(-x)$?", "options": ["$f(x)$", "$-f(x)$", "$|f(x)|$", r"$\frac{1}{f(x)}$"], "correctIndex": 1},
            {"id": 5, "question": "What does the graph $y = |x - 2|$ look like at $x = 2$?", "options": ["A smooth curve", "A corner/cusp pointing up", "A corner pointing down", "A vertical asymptote"], "correctIndex": 1},
            {"id": 6, "question": "How many solutions does $|2x - 3| = 5$ have?", "options": ["$0$", "$1$", "$2$", "Infinite"], "correctIndex": 2},
            {"id": 7, "question": "A graph has $x$-intercepts at $x = -1$ and $x = 3$ and passes through $(0, -6)$. Its equation is:", "options": ["$y = 2(x+1)(x-3)$", "$y = (x+1)(x-3)$", "$y = -(x+1)(x-3)$", "$y = 2(x-1)(x+3)$"], "correctIndex": 0},
            {"id": 8, "question": "For the parametric curve $x = t^2$, $y = 2t$, what is the Cartesian equation?", "options": ["$y^2 = 4x$", "$x^2 = 4y$", r"$y = 2\sqrt{x}$", r"$x = \frac{y^2}{4}$"], "correctIndex": 0},
            {"id": 9, "question": "What is the discriminant condition for $y = ax^2 + bx + c$ ($a > 0$) to not cross the $x$-axis?", "options": ["$b^2 - 4ac = 0$", "$b^2 - 4ac > 0$", "$b^2 - 4ac < 0$", "$b^2 + 4ac < 0$"], "correctIndex": 2},
            {"id": 10, "question": "The composite function $fg(x)$ means:", "options": ["$f(x) \\cdot g(x)$", "$g(f(x))$", "$f(g(x))$", "$f(x) + g(x)$"], "correctIndex": 2},
        ],
    },
    "Circles": {
        "Easy": [
            {"id": 1, "question": "What is the equation of a circle centred at the origin with radius $r$?", "options": ["$x + y = r$", "$x^2 + y^2 = r$", "$x^2 + y^2 = r^2$", "$(x-r)^2 + (y-r)^2 = 1$"], "correctIndex": 2},
            {"id": 2, "question": "Find the radius of $x^2 + y^2 = 49$", "options": ["$7$", "$49$", r"$\sqrt{49}$", "$7^2$"], "correctIndex": 0},
            {"id": 3, "question": "What is the centre of $(x-3)^2 + (y+2)^2 = 16$?", "options": ["$(3, 2)$", "$(-3, 2)$", "$(3, -2)$", "$(-3, -2)$"], "correctIndex": 2},
            {"id": 4, "question": "What is the radius of $(x-1)^2 + (y-1)^2 = 25$?", "options": ["$25$", "$5$", r"$\sqrt{5}$", "$10$"], "correctIndex": 1},
            {"id": 5, "question": "A tangent to a circle meets the radius at what angle?", "options": [r"$45°$", r"$60°$", r"$90°$", r"$180°$"], "correctIndex": 2},
            {"id": 6, "question": "Does the point $(3, 4)$ lie on $x^2 + y^2 = 25$?", "options": ["Yes", "No", "Only if extended", "Cannot tell"], "correctIndex": 0},
            {"id": 7, "question": "What is the diameter of a circle with radius $6$?", "options": ["$3$", "$6$", "$12$", "$36$"], "correctIndex": 2},
            {"id": 8, "question": "The angle in a semicircle is always:", "options": [r"$45°$", r"$60°$", r"$90°$", r"$180°$"], "correctIndex": 2},
            {"id": 9, "question": "What is the centre of $x^2 + y^2 + 4x - 6y = 0$?", "options": ["$(4, -6)$", "$(-2, 3)$", "$(2, -3)$", "$(-4, 6)$"], "correctIndex": 1},
            {"id": 10, "question": "Which form directly shows the centre and radius of a circle?", "options": ["General form", "Expanded form", "Standard (completed square) form", "Implicit form"], "correctIndex": 2},
        ],
        "Medium": [
            {"id": 1, "question": "Find the centre of $x^2 + y^2 - 6x + 2y - 15 = 0$", "options": ["$(-3, 1)$", "$(3, -1)$", "$(-6, 2)$", "$(6, -2)$"], "correctIndex": 1},
            {"id": 2, "question": "Find the radius of $x^2 + y^2 - 6x + 2y - 15 = 0$", "options": [r"$\sqrt{15}$", "$5$", "$25$", r"$\sqrt{25} = 5$"], "correctIndex": 3},
            {"id": 3, "question": "What is the equation of the tangent at $(3, 4)$ on $x^2 + y^2 = 25$?", "options": ["$3x + 4y = 25$", "$4x + 3y = 25$", "$3x - 4y = 25$", "$x + y = 7$"], "correctIndex": 0},
            {"id": 4, "question": "Two circles are concentric if they share the same:", "options": ["Radius", "Diameter", "Centre", "Chord"], "correctIndex": 2},
            {"id": 5, "question": "Find the length of the tangent from $(7, 0)$ to $x^2 + y^2 = 25$", "options": [r"$\sqrt{74}$", r"$\sqrt{24}$", r"$\sqrt{49-25}$", r"$\sqrt{49+25}$"], "correctIndex": 2},
            {"id": 6, "question": "The perpendicular from the centre of a circle to a chord always:", "options": ["Misses the chord", "Only bisects the diameter", "Bisects the chord", "Only applies to tangents"], "correctIndex": 2},
            {"id": 7, "question": "Does $y = x + 10$ intersect $x^2 + y^2 = 25$?", "options": ["Yes, twice", "Yes, once (tangent)", "No", "Cannot tell"], "correctIndex": 2},
            {"id": 8, "question": "The normal to a circle at a point passes through:", "options": ["The tangent", "The $y$-axis", "The centre", "Another point on the circle"], "correctIndex": 2},
            {"id": 9, "question": "What is the condition for $y = mx + c$ to be tangent to $x^2 + y^2 = r^2$?", "options": ["$c = r$", r"$c^2 = r^2(1 + m^2)$", r"$c^2 = r^2(m^2 - 1)$", "$m = r$"], "correctIndex": 1},
            {"id": 10, "question": r"Find the distance between the centres of $(x-1)^2+(y-2)^2=4$ and $(x-4)^2+(y-6)^2=9$", "options": ["$3$", "$4$", "$5$", "$7$"], "correctIndex": 2},
        ],
        "Hard": [
            {"id": 1, "question": "Find the equation of the circle with diameter endpoints $(1, 3)$ and $(5, 7)$", "options": ["$(x-3)^2+(y-5)^2=8$", "$(x-3)^2+(y-5)^2=4$", "$(x-2)^2+(y-4)^2=8$", "$(x-3)^2+(y-5)^2=16$"], "correctIndex": 0},
            {"id": 2, "question": "How many common tangents do two circles have if one is strictly inside the other?", "options": ["$0$", "$1$", "$2$", "$3$"], "correctIndex": 0},
            {"id": 3, "question": "For two intersecting circles, the radical axis is:", "options": ["A single point", "The common chord extended", "The line through both centres", "Outside both circles"], "correctIndex": 1},
            {"id": 4, "question": "Find where $x^2 + y^2 = 10$ and $y = x + 2$ intersect", "options": ["$(1, 3)$ and $(-3, -1)$", "$(1, 3)$ and $(3, -1)$", "$(-1, 3)$ and $(3, 1)$", "$(1, 3)$ only"], "correctIndex": 0},
            {"id": 5, "question": r"Two circles touch externally. If radii are $3$ and $5$, the distance between centres is:", "options": ["$2$", "$4$", "$8$", "$15$"], "correctIndex": 2},
            {"id": 6, "question": "A circle passes through $(0,0)$, $(4,0)$, and $(0,3)$. What is its centre?", "options": [r"$(2, 1.5)$", r"$\left(2, \frac{3}{2}\right)$", "Both A and B", "$(1, 2)$"], "correctIndex": 2},
            {"id": 7, "question": r"Find the angle subtended at the centre by a chord of length $6$ in a circle of radius $5$", "options": [r"$\arccos\frac{7}{25}$", r"$2\arcsin\frac{3}{5}$", r"$\arcsin\frac{3}{5}$", r"$2\arccos\frac{3}{5}$"], "correctIndex": 1},
            {"id": 8, "question": "What is the equation of the circle passing through $(1,1)$, $(1,-1)$, and $(3,1)$?", "options": ["$(x-2)^2+y^2=2$", "$(x-2)^2+y^2=1$", "$x^2+y^2=2$", "$(x-1)^2+y^2=1$"], "correctIndex": 0},
            {"id": 9, "question": "If the circle $x^2+y^2+Dx+Ey+F=0$ passes through the origin, then:", "options": ["$D=0$", "$E=0$", "$F=0$", "$D+E+F=0$"], "correctIndex": 2},
            {"id": 10, "question": "Two circles intersect at right angles if:", "options": [r"$r_1^2 + r_2^2 = d^2$", r"$r_1 + r_2 = d$", r"$r_1^2 - r_2^2 = d^2$", r"$d = r_1 - r_2$"], "correctIndex": 0},
        ],
    },
}

TOTAL_TIME = 90
TOTAL_LIVES = 3
TOTAL_QUESTIONS = 10


@anvil.server.callable
def get_topics():
    """Return list of available quiz topics with metadata."""
    return [
        {"name": "Differentiation", "description": "Rates of change & gradients", "icon": "trending-up", "color": "blue"},
        {"name": "Integration", "description": "Areas & anti-derivatives", "icon": "calculator", "color": "emerald"},
        {"name": "Graphs", "description": "Transformations & sketching", "icon": "book-open", "color": "violet"},
        {"name": "Circles", "description": "Equations & geometry", "icon": "circle", "color": "orange"},
    ]


@anvil.server.callable
def get_difficulties():
    """Return list of difficulty levels with metadata."""
    return [
        {"name": "Easy", "description": "Fundamental concepts & definitions", "icon": "zap", "color": "emerald"},
        {"name": "Medium", "description": "Applied techniques & problem solving", "icon": "star", "color": "amber"},
        {"name": "Hard", "description": "Complex proofs & challenging problems", "icon": "flame", "color": "red"},
    ]


@anvil.server.callable
def get_questions(topic, difficulty):
    """
    Return the 10 questions for a given topic and difficulty.
    Questions are returned as a list of dicts with question text,
    options list, and correctIndex.
    """
    if topic not in QUESTIONS:
        raise ValueError(f"Unknown topic: {topic}")
    if difficulty not in QUESTIONS[topic]:
        raise ValueError(f"Unknown difficulty: {difficulty}")
    return QUESTIONS[topic][difficulty]


@anvil.server.callable
def get_quiz_config():
    """Return quiz configuration constants."""
    return {
        "total_time": TOTAL_TIME,
        "total_lives": TOTAL_LIVES,
        "total_questions": TOTAL_QUESTIONS,
    }


@anvil.server.callable
def calculate_score(correct_answers, time_per_question_seconds):
    """
    Calculate score from a list of (is_correct, elapsed_seconds) tuples.
    Speed bonus: max(0, round((10 - elapsed) * 10)) added to base 100 per correct answer.
    """
    total_score = 0
    for is_correct, elapsed in zip(correct_answers, time_per_question_seconds):
        if is_correct:
            speed_bonus = max(0, round((10 - elapsed) * 10))
            total_score += 100 + speed_bonus
    return total_score


@anvil.server.callable
def save_quiz_result(topic, difficulty, score, correct_count, reason, time_used):
    """
    Persist a completed quiz result to the Data Table.
    Columns: topic, difficulty, score, correct_count, reason, time_used, completed_at
    """
    import datetime
    try:
        app_tables.quiz_results.add_row(
            topic=topic,
            difficulty=difficulty,
            score=score,
            correct_count=correct_count,
            reason=reason,
            time_used=time_used,
            completed_at=datetime.datetime.now(),
        )
        return True
    except Exception as e:
        print(f"Warning: could not save quiz result: {e}")
        return False


@anvil.server.callable
def get_leaderboard(topic=None, difficulty=None, limit=10):
    """
    Return top scores from the quiz_results table.
    Optionally filter by topic and/or difficulty.
    """
    try:
        rows = app_tables.quiz_results.search(
            tables.order_by("score", ascending=False)
        )
        results = []
        for row in rows:
            if topic and row["topic"] != topic:
                continue
            if difficulty and row["difficulty"] != difficulty:
                continue
            results.append({
                "topic": row["topic"],
                "difficulty": row["difficulty"],
                "score": row["score"],
                "correct_count": row["correct_count"],
                "reason": row["reason"],
                "time_used": row["time_used"],
                "completed_at": str(row["completed_at"]),
            })
            if len(results) >= limit:
                break
        return results
    except Exception as e:
        print(f"Warning: could not fetch leaderboard: {e}")
        return []
