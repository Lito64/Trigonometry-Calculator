import streamlit as st
import math
import re

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Trigonometry Calculator",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS STYLING
# ============================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .main-header {
        background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%);
        color: white;
        padding: 25px;
        border-radius: 12px;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 32px;
        font-weight: 700;
    }
    
    .main-header p {
        margin: 8px 0 0 0;
        opacity: 0.9;
        font-size: 16px;
    }
    
    .result-box {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 20px;
        border-left: 5px solid #8b5cf6;
        margin: 15px 0;
    }
    
    .result-value {
        font-size: 24px;
        font-weight: 700;
        color: #1e293b;
        text-align: center;
        padding: 15px;
        background: white;
        border-radius: 10px;
        margin: 10px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    
    .steps-box {
        background: #f0fdf4;
        border-radius: 10px;
        padding: 15px;
        border-left: 4px solid #10b981;
        margin-top: 15px;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        white-space: pre-wrap;
    }
    
    .info-box {
        background: #eff6ff;
        border-radius: 10px;
        padding: 15px;
        border-left: 4px solid #3b82f6;
        margin: 10px 0;
    }
    
    .warning-box {
        background: #fef3c7;
        border-radius: 10px;
        padding: 15px;
        border-left: 4px solid #f59e0b;
        margin: 10px 0;
    }
    
    .error-box {
        background: #fef2f2;
        border-radius: 10px;
        padding: 15px;
        border-left: 4px solid #ef4444;
        margin: 10px 0;
    }
    
    .metric-card {
        background: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        text-align: center;
        margin: 5px;
    }
    
    .metric-label {
        font-size: 12px;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-value {
        font-size: 20px;
        font-weight: 700;
        color: #1e293b;
        margin-top: 5px;
    }
    
    .section-header {
        font-size: 18px;
        font-weight: 600;
        color: #1e293b;
        margin: 20px 0 10px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid #e2e8f0;
    }
    
    div[data-testid="stExpander"] {
        background: white;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# CONSTANTS AND SPECIAL VALUES
# ============================================================

PI = math.pi

SPECIAL_ANGLES = {
    0: {'sin': '0', 'cos': '1', 'tan': '0'},
    30: {'sin': '1/2', 'cos': '√3/2', 'tan': '√3/3'},
    45: {'sin': '√2/2', 'cos': '√2/2', 'tan': '1'},
    60: {'sin': '√3/2', 'cos': '1/2', 'tan': '√3'},
    90: {'sin': '1', 'cos': '0', 'tan': 'undefined'},
    120: {'sin': '√3/2', 'cos': '-1/2', 'tan': '-√3'},
    135: {'sin': '√2/2', 'cos': '-√2/2', 'tan': '-1'},
    150: {'sin': '1/2', 'cos': '-√3/2', 'tan': '-√3/3'},
    180: {'sin': '0', 'cos': '-1', 'tan': '0'},
    210: {'sin': '-1/2', 'cos': '-√3/2', 'tan': '√3/3'},
    225: {'sin': '-√2/2', 'cos': '-√2/2', 'tan': '1'},
    240: {'sin': '-√3/2', 'cos': '-1/2', 'tan': '√3'},
    270: {'sin': '-1', 'cos': '0', 'tan': 'undefined'},
    300: {'sin': '-√3/2', 'cos': '1/2', 'tan': '-√3'},
    315: {'sin': '-√2/2', 'cos': '√2/2', 'tan': '-1'},
    330: {'sin': '-1/2', 'cos': '√3/2', 'tan': '-√3/3'},
    360: {'sin': '0', 'cos': '1', 'tan': '0'}
}

# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def parse_number(s):
    """Parse a number string that may contain √, π, or fractions."""
    if not s or str(s).strip() == '':
        return float('nan')
    s = str(s).strip()
    
    # Handle square roots
    s = re.sub(r'√(\d+)', lambda m: str(math.sqrt(float(m.group(1)))), s)
    s = re.sub(r'sqrt\((\d+)\)', lambda m: str(math.sqrt(float(m.group(1)))), s, flags=re.IGNORECASE)
    
    # Handle pi
    s = s.replace('π', str(PI)).replace('pi', str(PI)).replace('PI', str(PI))
    
    # Handle fractions
    if '/' in s:
        parts = s.split('/')
        if len(parts) == 2:
            try:
                return float(parts[0]) / float(parts[1])
            except:
                return float('nan')
    
    try:
        return float(s)
    except:
        return float('nan')

def to_radians(degrees):
    """Convert degrees to radians."""
    return degrees * PI / 180

def to_degrees(radians):
    """Convert radians to degrees."""
    return radians * 180 / PI

def format_number(n, decimals=6):
    """Format a number for display."""
    if abs(n) < 1e-10:
        return '0'
    result = round(n, decimals)
    if result == int(result):
        return str(int(result))
    return str(result).rstrip('0').rstrip('.')

def format_radians(r):
    """Format radians as a multiple of π if possible."""
    m = r / PI
    fracs = [(1,6), (1,4), (1,3), (1,2), (2,3), (3,4), (5,6), (1,1), 
             (7,6), (5,4), (4,3), (3,2), (5,3), (7,4), (11,6), (2,1)]
    
    for n, d in fracs:
        if abs(m - n/d) < 0.0001:
            if n == 1 and d == 1:
                return 'π'
            elif d == 1:
                return f'{n}π'
            elif n == 1:
                return f'π/{d}'
            else:
                return f'{n}π/{d}'
        if abs(m + n/d) < 0.0001:
            if n == 1 and d == 1:
                return '-π'
            elif d == 1:
                return f'-{n}π'
            elif n == 1:
                return f'-π/{d}'
            else:
                return f'-{n}π/{d}'
    
    return f'{format_number(r)} rad'

def get_quadrant(degrees):
    """Get the quadrant for an angle in degrees."""
    n = ((degrees % 360) + 360) % 360
    if n == 0 or n == 360:
        return '+x axis'
    elif n == 90:
        return '+y axis'
    elif n == 180:
        return '-x axis'
    elif n == 270:
        return '-y axis'
    elif n < 90:
        return 'I'
    elif n < 180:
        return 'II'
    elif n < 270:
        return 'III'
    else:
        return 'IV'

def get_reference_angle(degrees):
    """Get the reference angle in degrees."""
    n = ((degrees % 360) + 360) % 360
    if n <= 90:
        return n
    elif n <= 180:
        return 180 - n
    elif n <= 270:
        return n - 180
    else:
        return 360 - n

def get_exact_value(degrees, func):
    """Get the exact value for special angles."""
    n = ((round(degrees) % 360) + 360) % 360
    if n in SPECIAL_ANGLES and func in SPECIAL_ANGLES[n]:
        return SPECIAL_ANGLES[n][func]
    return None

def format_complex(re_part, im_part):
    """Format a complex number for display."""
    if abs(im_part) < 1e-10:
        return format_number(re_part)
    if abs(re_part) < 1e-10:
        return f"{format_number(im_part)}i"
    sign = '+' if im_part >= 0 else '-'
    return f"{format_number(re_part)} {sign} {format_number(abs(im_part))}i"

# ============================================================
# SIDEBAR CONFIGURATION
# ============================================================

with st.sidebar:
    st.markdown("### ⚙️ Settings")
    
    # Calculator level selection
    calc_level = st.radio(
        "Calculator Level",
        ["📚 Foundations", "🎓 Advanced"],
        index=0
    )
    
    st.markdown("---")
    
    # Angle mode
    angle_mode = st.radio(
        "Angle Mode",
        ["Degrees (DEG)", "Radians (RAD)"],
        index=0
    )
    use_radians = "RAD" in angle_mode
    
    # Show steps toggle
    show_steps = st.checkbox("Show Step-by-Step Solutions", value=True)
    
    st.markdown("---")
    
    # Quick reference
    with st.expander("📋 Quick Reference"):
        st.markdown("""
        **Pythagorean Identity:**
        - sin²θ + cos²θ = 1
        
        **Reciprocal:**
        - csc θ = 1/sin θ
        - sec θ = 1/cos θ
        - cot θ = 1/tan θ
        
        **Quotient:**
        - tan θ = sin θ/cos θ
        - cot θ = cos θ/sin θ
        
        **Special Angles:**
        - 30° = π/6
        - 45° = π/4
        - 60° = π/3
        - 90° = π/2
        """)

# ============================================================
# HEADER
# ============================================================

level_emoji = "📚" if "Foundations" in calc_level else "🎓"
level_name = "Foundations" if "Foundations" in calc_level else "Advanced"

st.markdown(f"""
<div class="main-header">
    <h1>{level_emoji} Trigonometry Calculator</h1>
    <p>{level_name} Level • {"Radians" if use_radians else "Degrees"} Mode</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# FOUNDATIONS CALCULATOR
# ============================================================

if "Foundations" in calc_level:
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📐 Angles & Arcs",
        "📏 Right Triangles", 
        "📊 Trig Evaluator",
        "🌊 Sinusoidal Functions",
        "🔺 Oblique Triangles"
    ])
    
    # ==================== TAB 1: ANGLES & ARCS ====================
    with tab1:
        section = st.radio(
            "Select Section",
            ["Angle Conversions", "Arc Length & Sector", "Linear & Angular Speed"],
            horizontal=True,
            key="angles_section"
        )
        
        if section == "Angle Conversions":
            st.markdown('<div class="section-header">📐 Angle Conversions</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                angle_input = st.text_input("Enter Angle", placeholder="e.g., 45, π/3, 45.5", key="angle_conv_input")
            with col2:
                input_format = st.selectbox("Input Format", ["Degrees", "Radians"], key="angle_conv_format")
            
            if st.button("Convert", key="convert_angle"):
                if angle_input:
                    try:
                        value = parse_number(angle_input)
                        if math.isnan(value):
                            st.error("Invalid input. Please enter a valid number.")
                        else:
                            # Convert to degrees for calculations
                            if input_format == "Radians":
                                degrees = to_degrees(value)
                                radians = value
                            else:
                                degrees = value
                                radians = to_radians(value)
                            
                            quadrant = get_quadrant(degrees)
                            ref_angle = get_reference_angle(degrees)
                            
                            # DMS conversion
                            abs_deg = abs(degrees)
                            d = int(abs_deg)
                            m_float = (abs_deg - d) * 60
                            m = int(m_float)
                            s = (m_float - m) * 60
                            sign = "-" if degrees < 0 else ""
                            
                            # Display results
                            st.markdown('<div class="result-box">', unsafe_allow_html=True)
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Degrees", f"{format_number(degrees)}°")
                            with col2:
                                st.metric("Radians", format_radians(radians))
                            with col3:
                                st.metric("DMS", f'{sign}{d}° {m}\' {format_number(s, 2)}"')
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Quadrant", quadrant)
                            with col2:
                                st.metric("Reference Angle", f"{format_number(ref_angle)}°")
                            with col3:
                                st.metric("Coterminal (+360°)", f"{format_number(degrees + 360)}°")
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                            
                            if show_steps:
                                steps = f"""Given: {angle_input} ({input_format.lower()})

Step 1: Convert to decimal degrees
  {angle_input} = {format_number(degrees)}°

Step 2: Convert to radians
  Radians = Degrees × (π/180)
  {format_number(degrees)}° × (π/180) = {format_number(radians)} rad
  = {format_radians(radians)}

Step 3: Find the quadrant
  Normalize: {format_number(degrees)}° mod 360° = {format_number(((degrees % 360) + 360) % 360)}°
  This angle is in Quadrant {quadrant}

Step 4: Find the reference angle
  Reference angle = {format_number(ref_angle)}°

Step 5: Convert to DMS
  {format_number(degrees)}° = {sign}{d}° {m}' {format_number(s, 2)}\""""
                                st.markdown(f'<div class="steps-box">{steps}</div>', unsafe_allow_html=True)
                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        elif section == "Arc Length & Sector":
            st.markdown('<div class="section-header">⌒ Arc Length & Sector Area</div>', unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                radius = st.text_input("Radius (r)", placeholder="e.g., 5", key="arc_radius")
            with col2:
                arc_angle = st.text_input("Central Angle (θ)", placeholder="e.g., π/4 or 45", key="arc_angle")
            with col3:
                arc_unit = st.selectbox("Angle Unit", ["Radians", "Degrees"], key="arc_unit")
            
            if st.button("Calculate", key="calc_arc"):
                r = parse_number(radius)
                theta = parse_number(arc_angle)
                
                if math.isnan(r) or math.isnan(theta) or r <= 0:
                    st.error("Please enter valid positive values.")
                else:
                    # Convert to radians if needed
                    theta_rad = theta if arc_unit == "Radians" else to_radians(theta)
                    
                    arc_length = r * theta_rad
                    sector_area = 0.5 * r * r * theta_rad
                    circumference = 2 * PI * r
                    circle_area = PI * r * r
                    
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Arc Length (s)", f"{format_number(arc_length)} units")
                        st.metric("Full Circumference", f"{format_number(circumference)} units")
                    with col2:
                        st.metric("Sector Area (A)", f"{format_number(sector_area)} sq units")
                        st.metric("Full Circle Area", f"{format_number(circle_area)} sq units")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    if show_steps:
                        steps = f"""Given:
  Radius r = {radius}
  Central angle θ = {arc_angle} {arc_unit.lower()}
  {'  → θ in radians = ' + str(arc_angle) + '° × (π/180) = ' + format_number(theta_rad) + ' rad' if arc_unit == 'Degrees' else ''}

Step 1: Calculate Arc Length
  Formula: s = rθ (θ must be in radians)
  s = {r} × {format_number(theta_rad)}
  s = {format_number(arc_length)} units

Step 2: Calculate Sector Area
  Formula: A = ½r²θ (θ must be in radians)
  A = ½ × {r}² × {format_number(theta_rad)}
  A = ½ × {format_number(r * r)} × {format_number(theta_rad)}
  A = {format_number(sector_area)} square units

Step 3: Comparison with full circle
  Full circumference = 2πr = 2π × {r} = {format_number(circumference)}
  Arc is {format_number(arc_length / circumference * 100)}% of circumference
  
  Full area = πr² = π × {r}² = {format_number(circle_area)}
  Sector is {format_number(sector_area / circle_area * 100)}% of circle"""
                        st.markdown(f'<div class="steps-box">{steps}</div>', unsafe_allow_html=True)
        
        else:  # Linear & Angular Speed
            st.markdown('<div class="section-header">⟳ Linear & Angular Speed</div>', unsafe_allow_html=True)
            st.info("Enter any two values to solve for the third (v = rω)")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                speed_radius = st.text_input("Radius (r)", placeholder="e.g., 2", key="speed_r")
                speed_r_unit = st.selectbox("Unit", ["meters", "cm", "feet"], key="speed_r_unit")
            
            with col2:
                speed_omega = st.text_input("Angular Speed (ω)", placeholder="e.g., 3", key="speed_omega")
                speed_w_unit = st.selectbox("Unit", ["rad/s", "rpm", "deg/s"], key="speed_w_unit")
            
            with col3:
                speed_linear = st.text_input("Linear Speed (v)", placeholder="e.g., 6", key="speed_v")
                speed_v_unit = st.selectbox("Unit", ["m/s", "km/h", "mph"], key="speed_v_unit")
            
            if st.button("Calculate", key="calc_speed"):
                r = parse_number(speed_radius) if speed_radius else float('nan')
                w = parse_number(speed_omega) if speed_omega else float('nan')
                v = parse_number(speed_linear) if speed_linear else float('nan')
                
                count = sum([not math.isnan(x) for x in [r, w, v]])
                
                if count < 2:
                    st.error("Please enter at least two values.")
                else:
                    # Unit conversions to SI
                    r_conv = {'meters': 1, 'cm': 0.01, 'feet': 0.3048}
                    w_conv = {'rad/s': 1, 'rpm': 2 * PI / 60, 'deg/s': PI / 180}
                    v_conv = {'m/s': 1, 'km/h': 1/3.6, 'mph': 0.44704}
                    
                    # Convert to base units
                    r_base = r * r_conv[speed_r_unit] if not math.isnan(r) else float('nan')
                    w_base = w * w_conv[speed_w_unit] if not math.isnan(w) else float('nan')
                    v_base = v * v_conv[speed_v_unit] if not math.isnan(v) else float('nan')
                    
                    if math.isnan(r):
                        r_base = v_base / w_base
                        r = r_base / r_conv[speed_r_unit]
                        solved = "radius"
                    elif math.isnan(w):
                        w_base = v_base / r_base
                        w = w_base / w_conv[speed_w_unit]
                        solved = "angular speed"
                    else:
                        v_base = r_base * w_base
                        v = v_base / v_conv[speed_v_unit]
                        solved = "linear speed"
                    
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Radius", f"{format_number(r)} {speed_r_unit}")
                    with col2:
                        st.metric("Angular Speed", f"{format_number(w)} {speed_w_unit}")
                    with col3:
                        st.metric("Linear Speed", f"{format_number(v)} {speed_v_unit}")
                    st.success(f"Solved for: {solved}")
                    st.markdown('</div>', unsafe_allow_html=True)
    
    # ==================== TAB 2: RIGHT TRIANGLES ====================
    with tab2:
        section = st.radio(
            "Select Section",
            ["Triangle Solver", "Applications"],
            horizontal=True,
            key="right_section"
        )
        
        if section == "Triangle Solver":
            st.markdown('<div class="section-header">📐 Right Triangle Solver</div>', unsafe_allow_html=True)
            st.info("Enter at least 2 values (including at least one side). Side c is the hypotenuse.")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Sides**")
                rt_a = st.text_input("Side a (opposite to A)", placeholder="e.g., 3", key="rt_a")
                rt_b = st.text_input("Side b (adjacent to A)", placeholder="e.g., 4", key="rt_b")
                rt_c = st.text_input("Side c (hypotenuse)", placeholder="e.g., 5", key="rt_c")
            
            with col2:
                st.markdown("**Angles**")
                angle_unit_label = "radians" if use_radians else "degrees"
                rt_A = st.text_input(f"Angle A ({angle_unit_label})", placeholder="e.g., 30", key="rt_A")
                rt_B = st.text_input(f"Angle B ({angle_unit_label})", placeholder="e.g., 60", key="rt_B")
                st.text("Angle C = 90° (right angle)")
            
            if st.button("Solve Triangle", key="solve_rt"):
                a = parse_number(rt_a) if rt_a else float('nan')
                b = parse_number(rt_b) if rt_b else float('nan')
                c = parse_number(rt_c) if rt_c else float('nan')
                A = parse_number(rt_A) if rt_A else float('nan')
                B = parse_number(rt_B) if rt_B else float('nan')
                
                # Convert angles to degrees if in radians mode
                if use_radians:
                    A = to_degrees(A) if not math.isnan(A) else float('nan')
                    B = to_degrees(B) if not math.isnan(B) else float('nan')
                
                sides_count = sum([not math.isnan(x) for x in [a, b, c]])
                angles_count = sum([not math.isnan(x) for x in [A, B]])
                
                if sides_count == 0:
                    st.error("At least one side is required.")
                elif sides_count + angles_count < 2:
                    st.error("Please provide at least two values.")
                else:
                    try:
                        steps = ""
                        
                        if sides_count == 2:
                            if not math.isnan(a) and not math.isnan(b):
                                c = math.sqrt(a*a + b*b)
                                steps = f"Given: a = {a}, b = {b}\n\nStep 1: Find hypotenuse c using Pythagorean theorem\n  c² = a² + b² = {a}² + {b}² = {format_number(a*a + b*b)}\n  c = √{format_number(a*a + b*b)} = {format_number(c)}"
                            elif not math.isnan(a) and not math.isnan(c):
                                if a >= c:
                                    raise ValueError("Side a must be less than hypotenuse c")
                                b = math.sqrt(c*c - a*a)
                                steps = f"Given: a = {a}, c = {c}\n\nStep 1: Find side b\n  b² = c² - a² = {c}² - {a}² = {format_number(c*c - a*a)}\n  b = √{format_number(c*c - a*a)} = {format_number(b)}"
                            else:
                                if b >= c:
                                    raise ValueError("Side b must be less than hypotenuse c")
                                a = math.sqrt(c*c - b*b)
                                steps = f"Given: b = {b}, c = {c}\n\nStep 1: Find side a\n  a² = c² - b² = {c}² - {b}² = {format_number(c*c - b*b)}\n  a = √{format_number(c*c - b*b)} = {format_number(a)}"
                            
                            A = to_degrees(math.asin(max(-1, min(1, a / c))))
                            B = 90 - A
                            steps += f"\n\nStep 2: Find angle A\n  sin(A) = a/c = {format_number(a)}/{format_number(c)} = {format_number(a/c)}\n  A = arcsin({format_number(a/c)}) = {format_number(A)}°"
                            steps += f"\n\nStep 3: Find angle B\n  B = 90° - A = 90° - {format_number(A)}° = {format_number(B)}°"
                        
                        elif sides_count == 1 and angles_count >= 1:
                            if not math.isnan(A):
                                B = 90 - A
                            else:
                                A = 90 - B
                            
                            A_rad = to_radians(A)
                            
                            if not math.isnan(a):
                                c = a / math.sin(A_rad)
                                b = a / math.tan(A_rad)
                                steps = f"Given: a = {a}, A = {format_number(A)}°\n\nStep 1: Find B = 90° - A = {format_number(B)}°"
                                steps += f"\n\nStep 2: Find c = a/sin(A) = {a}/sin({format_number(A)}°) = {format_number(c)}"
                                steps += f"\n\nStep 3: Find b = a/tan(A) = {a}/tan({format_number(A)}°) = {format_number(b)}"
                            elif not math.isnan(b):
                                c = b / math.cos(A_rad)
                                a = b * math.tan(A_rad)
                                steps = f"Given: b = {b}, A = {format_number(A)}°\n\nStep 1: Find B = 90° - A = {format_number(B)}°"
                                steps += f"\n\nStep 2: Find c = b/cos(A) = {b}/cos({format_number(A)}°) = {format_number(c)}"
                                steps += f"\n\nStep 3: Find a = b×tan(A) = {b}×tan({format_number(A)}°) = {format_number(a)}"
                            else:
                                a = c * math.sin(A_rad)
                                b = c * math.cos(A_rad)
                                steps = f"Given: c = {c}, A = {format_number(A)}°\n\nStep 1: Find B = 90° - A = {format_number(B)}°"
                                steps += f"\n\nStep 2: Find a = c×sin(A) = {c}×sin({format_number(A)}°) = {format_number(a)}"
                                steps += f"\n\nStep 3: Find b = c×cos(A) = {c}×cos({format_number(A)}°) = {format_number(b)}"
                        
                        area = 0.5 * a * b
                        steps += f"\n\nStep 4: Calculate Area\n  Area = ½ × a × b = ½ × {format_number(a)} × {format_number(b)} = {format_number(area)} sq units"
                        
                        # Display results
                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Side a", format_number(a))
                            st.metric("Angle A", f"{format_number(A)}°")
                        with col2:
                            st.metric("Side b", format_number(b))
                            st.metric("Angle B", f"{format_number(B)}°")
                        with col3:
                            st.metric("Side c (hyp)", format_number(c))
                            st.metric("Area", f"{format_number(area)} sq units")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Trig ratios
                        st.markdown("**Trigonometric Ratios at Angle A:**")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            exact_sin = get_exact_value(A, 'sin')
                            st.metric("sin A", f"{exact_sin if exact_sin else format_number(math.sin(to_radians(A)))}")
                        with col2:
                            exact_cos = get_exact_value(A, 'cos')
                            st.metric("cos A", f"{exact_cos if exact_cos else format_number(math.cos(to_radians(A)))}")
                        with col3:
                            exact_tan = get_exact_value(A, 'tan')
                            val = math.tan(to_radians(A)) if A != 90 else float('inf')
                            st.metric("tan A", f"{exact_tan if exact_tan else format_number(val) if val != float('inf') else 'undefined'}")
                        
                        if show_steps:
                            st.markdown(f'<div class="steps-box">{steps}</div>', unsafe_allow_html=True)
                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        else:  # Applications
            st.markdown('<div class="section-header">🎯 Application Problems</div>', unsafe_allow_html=True)
            
            app_type = st.radio(
                "Problem Type",
                ["Angle of Elevation", "Angle of Depression", "Bearing"],
                horizontal=True,
                key="app_type"
            )
            
            if app_type == "Angle of Elevation":
                col1, col2 = st.columns(2)
                with col1:
                    app_dist = st.text_input("Horizontal Distance", placeholder="e.g., 100", key="app_dist")
                with col2:
                    app_angle = st.text_input("Angle of Elevation (degrees)", placeholder="e.g., 30", key="app_elev_angle")
                
                if st.button("Calculate Height", key="calc_elevation"):
                    d = parse_number(app_dist)
                    ang = parse_number(app_angle)
                    
                    if math.isnan(d) or math.isnan(ang):
                        st.error("Please enter both distance and angle.")
                    else:
                        height = d * math.tan(to_radians(ang))
                        
                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        st.metric("Height", f"{format_number(height)} units")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        if show_steps:
                            steps = f"""Angle of Elevation Problem

Given:
  Horizontal distance = {d} units
  Angle of elevation = {ang}°

Step 1: Set up the right triangle
  • The horizontal distance is the adjacent side
  • The height is the opposite side
  • The angle is measured from horizontal upward

Step 2: Use tangent ratio
  tan(θ) = opposite/adjacent = height/distance
  tan({ang}°) = height/{d}

Step 3: Solve for height
  height = distance × tan(θ)
  height = {d} × tan({ang}°)
  height = {d} × {format_number(math.tan(to_radians(ang)))}
  height = {format_number(height)} units"""
                            st.markdown(f'<div class="steps-box">{steps}</div>', unsafe_allow_html=True)
            
            elif app_type == "Angle of Depression":
                col1, col2 = st.columns(2)
                with col1:
                    app_height = st.text_input("Observer Height", placeholder="e.g., 50", key="app_height")
                with col2:
                    app_angle = st.text_input("Angle of Depression (degrees)", placeholder="e.g., 25", key="app_dep_angle")
                
                if st.button("Calculate Distance", key="calc_depression"):
                    h = parse_number(app_height)
                    ang = parse_number(app_angle)
                    
                    if math.isnan(h) or math.isnan(ang):
                        st.error("Please enter both height and angle.")
                    else:
                        distance = h / math.tan(to_radians(ang))
                        
                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        st.metric("Horizontal Distance", f"{format_number(distance)} units")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        if show_steps:
                            steps = f"""Angle of Depression Problem

Given:
  Observer height = {h} units
  Angle of depression = {ang}°

Step 1: Set up the right triangle
  • The height is the opposite side
  • The horizontal distance is the adjacent side
  • Angle of depression = angle of elevation (alternate interior angles)

Step 2: Use tangent ratio
  tan(θ) = opposite/adjacent = height/distance
  tan({ang}°) = {h}/distance

Step 3: Solve for distance
  distance = height/tan(θ)
  distance = {h}/tan({ang}°)
  distance = {h}/{format_number(math.tan(to_radians(ang)))}
  distance = {format_number(distance)} units"""
                            st.markdown(f'<div class="steps-box">{steps}</div>', unsafe_allow_html=True)
            
            else:  # Bearing
                col1, col2 = st.columns(2)
                with col1:
                    app_dist = st.text_input("Distance Traveled", placeholder="e.g., 10", key="bearing_dist")
                with col2:
                    app_bearing = st.text_input("Bearing", placeholder="e.g., N30°E or 30", key="bearing_angle")
                
                if st.button("Calculate Components", key="calc_bearing"):
                    d = parse_number(app_dist)
                    bearing_str = app_bearing.strip() if app_bearing else ""
                    
                    if math.isnan(d) or not bearing_str:
                        st.error("Please enter distance and bearing.")
                    else:
                        # Parse bearing
                        match = re.match(r'([NS])(\d+)[°]?([EW])', bearing_str, re.IGNORECASE)
                        if match:
                            ns = match.group(1).upper()
                            angle = float(match.group(2))
                            ew = match.group(3).upper()
                            
                            if ns == 'N' and ew == 'E':
                                bearing = angle
                            elif ns == 'S' and ew == 'E':
                                bearing = 180 - angle
                            elif ns == 'S' and ew == 'W':
                                bearing = 180 + angle
                            else:  # N and W
                                bearing = 360 - angle
                        else:
                            bearing = parse_number(bearing_str)
                        
                        if math.isnan(bearing):
                            st.error("Invalid bearing format. Use 'N30°E' or numeric degrees.")
                        else:
                            ns_comp = d * math.cos(to_radians(bearing))
                            ew_comp = d * math.sin(to_radians(bearing))
                            
                            st.markdown('<div class="result-box">', unsafe_allow_html=True)
                            col1, col2 = st.columns(2)
                            with col1:
                                ns_dir = "N" if ns_comp >= 0 else "S"
                                st.metric("North/South", f"{format_number(abs(ns_comp))} {ns_dir}")
                            with col2:
                                ew_dir = "E" if ew_comp >= 0 else "W"
                                st.metric("East/West", f"{format_number(abs(ew_comp))} {ew_dir}")
                            st.markdown('</div>', unsafe_allow_html=True)
    
    # ==================== TAB 3: TRIG EVALUATOR ====================
    with tab3:
        section = st.radio(
            "Select Section",
            ["Basic Functions", "Inverse Functions", "Compositions"],
            horizontal=True,
            key="eval_section"
        )
        
        if section == "Basic Functions":
            st.markdown('<div class="section-header">📊 Evaluate Trig Functions</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                trig_func = st.selectbox("Function", ["sin", "cos", "tan", "csc", "sec", "cot"], key="trig_func")
            with col2:
                angle_label = "radians" if use_radians else "degrees"
                trig_angle = st.text_input(f"Angle ({angle_label})", placeholder="e.g., 45 or π/4", key="trig_angle")
            
            if st.button("Evaluate", key="eval_trig"):
                if trig_angle:
                    try:
                        angle_val = parse_number(trig_angle)
                        
                        if math.isnan(angle_val):
                            st.error("Invalid angle input.")
                        else:
                            # Convert to degrees for calculations
                            if use_radians:
                                degrees = to_degrees(angle_val)
                            else:
                                degrees = angle_val
                            
                            radians = to_radians(degrees)
                            
                            # Calculate value
                            if trig_func == 'sin':
                                value = math.sin(radians)
                            elif trig_func == 'cos':
                                value = math.cos(radians)
                            elif trig_func == 'tan':
                                if abs(math.cos(radians)) < 1e-10:
                                    st.error("Tangent is undefined at this angle.")
                                    value = None
                                else:
                                    value = math.tan(radians)
                            elif trig_func == 'csc':
                                if abs(math.sin(radians)) < 1e-10:
                                    st.error("Cosecant is undefined at this angle.")
                                    value = None
                                else:
                                    value = 1 / math.sin(radians)
                            elif trig_func == 'sec':
                                if abs(math.cos(radians)) < 1e-10:
                                    st.error("Secant is undefined at this angle.")
                                    value = None
                                else:
                                    value = 1 / math.cos(radians)
                            else:  # cot
                                if abs(math.sin(radians)) < 1e-10:
                                    st.error("Cotangent is undefined at this angle.")
                                    value = None
                                else:
                                    value = 1 / math.tan(radians)
                            
                            if value is not None:
                                exact = get_exact_value(degrees, trig_func) if trig_func in ['sin', 'cos', 'tan'] else None
                                quadrant = get_quadrant(degrees)
                                ref_angle = get_reference_angle(degrees)
                                
                                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                                
                                col1, col2 = st.columns(2)
                                with col1:
                                    if exact:
                                        st.metric(f"{trig_func}({format_number(degrees)}°)", exact)
                                    st.metric("Decimal Value", format_number(value, 10))
                                with col2:
                                    st.metric("Quadrant", quadrant)
                                    st.metric("Reference Angle", f"{format_number(ref_angle)}°")
                                
                                st.markdown('</div>', unsafe_allow_html=True)
                                
                                if show_steps:
                                    steps = f"""Evaluating {trig_func}({trig_angle})

Step 1: Convert to degrees
  θ = {format_number(degrees)}°

Step 2: Find reference angle
  Quadrant: {quadrant}
  Reference angle: {format_number(ref_angle)}°

Step 3: Evaluate
  {trig_func}({format_number(degrees)}°) = {exact if exact else format_number(value, 10)}
  ≈ {format_number(value, 10)}"""
                                    st.markdown(f'<div class="steps-box">{steps}</div>', unsafe_allow_html=True)
                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        elif section == "Inverse Functions":
            st.markdown('<div class="section-header">🔄 Inverse Trig Functions</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                inv_func = st.selectbox("Function", ["arcsin", "arccos", "arctan", "arccsc", "arcsec", "arccot"], key="inv_func")
            with col2:
                inv_value = st.text_input("Value (x)", placeholder="e.g., 0.5", key="inv_value")
            
            if st.button("Evaluate", key="eval_inv"):
                if inv_value:
                    try:
                        x = parse_number(inv_value)
                        
                        if math.isnan(x):
                            st.error("Invalid input.")
                        else:
                            result = None
                            error = None
                            
                            if inv_func == 'arcsin':
                                if x < -1 or x > 1:
                                    error = "Value must be in [-1, 1]"
                                else:
                                    result = math.asin(x)
                            elif inv_func == 'arccos':
                                if x < -1 or x > 1:
                                    error = "Value must be in [-1, 1]"
                                else:
                                    result = math.acos(x)
                            elif inv_func == 'arctan':
                                result = math.atan(x)
                            elif inv_func == 'arccsc':
                                if -1 < x < 1:
                                    error = "Value must satisfy |x| ≥ 1"
                                else:
                                    result = math.asin(1 / x)
                            elif inv_func == 'arcsec':
                                if -1 < x < 1:
                                    error = "Value must satisfy |x| ≥ 1"
                                else:
                                    result = math.acos(1 / x)
                            else:  # arccot
                                result = math.atan(1 / x)
                                if x < 0:
                                    result += PI
                            
                            if error:
                                st.error(error)
                            else:
                                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                                
                                col1, col2 = st.columns(2)
                                with col1:
                                    st.metric("Radians", format_radians(result))
                                with col2:
                                    st.metric("Degrees", f"{format_number(to_degrees(result))}°")
                                
                                st.markdown('</div>', unsafe_allow_html=True)
                                
                                if show_steps:
                                    steps = f"""Evaluating {inv_func}({x})

Step 1: Check domain
  {inv_func}(x) requires valid input ✓

Step 2: Calculate result
  θ = {inv_func}({x})
  θ = {format_number(result)} radians
  θ = {format_radians(result)}

Step 3: Convert to degrees
  θ = {format_number(result)} × (180/π)
  θ = {format_number(to_degrees(result))}°"""
                                    st.markdown(f'<div class="steps-box">{steps}</div>', unsafe_allow_html=True)
                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        else:  # Compositions
            st.markdown('<div class="section-header">🔗 Function Compositions</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                comp_type = st.selectbox(
                    "Composition Type",
                    ["sin(arccos(x))", "cos(arcsin(x))", "tan(arcsin(x))", "tan(arccos(x))", "sin(arctan(x))", "cos(arctan(x))"],
                    key="comp_type"
                )
            with col2:
                comp_value = st.text_input("Value (x)", placeholder="e.g., 0.6", key="comp_value")
            
            if st.button("Evaluate", key="eval_comp"):
                if comp_value:
                    try:
                        x = parse_number(comp_value)
                        
                        if math.isnan(x):
                            st.error("Invalid input.")
                        else:
                            result = None
                            error = None
                            
                            if comp_type == "sin(arccos(x))":
                                if x < -1 or x > 1:
                                    error = "arccos needs x ∈ [-1, 1]"
                                else:
                                    result = math.sqrt(1 - x*x)
                            elif comp_type == "cos(arcsin(x))":
                                if x < -1 or x > 1:
                                    error = "arcsin needs x ∈ [-1, 1]"
                                else:
                                    result = math.sqrt(1 - x*x)
                            elif comp_type == "tan(arcsin(x))":
                                if x <= -1 or x >= 1:
                                    error = "Need x ∈ (-1, 1)"
                                else:
                                    result = x / math.sqrt(1 - x*x)
                            elif comp_type == "tan(arccos(x))":
                                if x <= -1 or x > 1 or x == 0:
                                    error = "Invalid domain"
                                else:
                                    result = math.sqrt(1 - x*x) / x
                            elif comp_type == "sin(arctan(x))":
                                result = x / math.sqrt(1 + x*x)
                            else:  # cos(arctan(x))
                                result = 1 / math.sqrt(1 + x*x)
                            
                            if error:
                                st.error(error)
                            else:
                                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                                st.metric(comp_type.replace("x", str(x)), format_number(result))
                                st.markdown('</div>', unsafe_allow_html=True)
                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
    
    # ==================== TAB 4: SINUSOIDAL FUNCTIONS ====================
    with tab4:
        section = st.radio(
            "Select Section",
            ["Parse Equation", "Build Equation", "Real-World Model"],
            horizontal=True,
            key="sin_section"
        )
        
        if section == "Parse Equation":
            st.markdown('<div class="section-header">📝 Parse Sinusoidal Equation</div>', unsafe_allow_html=True)
            st.info("Standard form: y = A sin(B(x - C)) + D or y = A cos(B(x - C)) + D")
            
            equation = st.text_input("Enter Equation", placeholder="e.g., y = 2sin(3x - π/2) + 1", key="parse_eq")
            
            if st.button("Parse", key="parse_sinusoidal"):
                if equation:
                    try:
                        eq = equation.lower().replace(' ', '')
                        func_type = 'cos' if 'cos' in eq else 'sin'
                        
                        # Parse amplitude
                        A = 1
                        amp_match = re.search(r'=(-?\d*\.?\d*)(sin|cos)', eq)
                        if amp_match and amp_match.group(1):
                            A = float(amp_match.group(1)) if amp_match.group(1) not in ['', '-'] else (1 if amp_match.group(1) == '' else -1)
                        
                        # Parse B
                        B = 1
                        b_match = re.search(r'(sin|cos)\((-?\d*\.?\d*)x', eq)
                        if b_match and b_match.group(2):
                            B = float(b_match.group(2)) if b_match.group(2) not in ['', '-'] else (1 if b_match.group(2) == '' else -1)
                        
                        # Parse phase shift (simplified)
                        C = 0
                        
                        # Parse vertical shift
                        D = 0
                        d_match = re.search(r'\)([+-])(\d+\.?\d*)$', eq)
                        if d_match:
                            D = float(d_match.group(2))
                            if d_match.group(1) == '-':
                                D = -D
                        
                        period = 2 * PI / abs(B)
                        amplitude = abs(A)
                        
                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("Function Type", func_type)
                            st.metric("Amplitude |A|", format_number(amplitude))
                            st.metric("B value", format_number(B))
                            st.metric("Period (2π/|B|)", format_radians(period))
                        with col2:
                            st.metric("Phase Shift (C)", format_number(C))
                            st.metric("Vertical Shift (D)", format_number(D))
                            st.metric("Maximum", format_number(D + amplitude))
                            st.metric("Minimum", format_number(D - amplitude))
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                    
                    except Exception as e:
                        st.error(f"Could not parse equation. Please use format: y = A sin(Bx) + D")
        
        elif section == "Build Equation":
            st.markdown('<div class="section-header">🔧 Build Equation from Parameters</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                build_func = st.selectbox("Function", ["sin", "cos"], key="build_func")
                build_A = st.text_input("Amplitude (A)", placeholder="e.g., 2", key="build_A")
                build_period = st.text_input("Period", placeholder="e.g., 2π or 360", key="build_period")
            with col2:
                build_C = st.text_input("Phase Shift (C)", placeholder="e.g., 0", key="build_C")
                build_D = st.text_input("Vertical Shift (D)", placeholder="e.g., 0", key="build_D")
            
            if st.button("Build Equation", key="build_eq"):
                A = parse_number(build_A) if build_A else 1
                period = parse_number(build_period)
                C = parse_number(build_C) if build_C else 0
                D = parse_number(build_D) if build_D else 0
                
                if math.isnan(period) or period == 0:
                    st.error("Please enter a valid period.")
                else:
                    B = 2 * PI / period
                    
                    # Build equation string
                    eq_parts = ["y = "]
                    if A != 1:
                        eq_parts.append(str(format_number(A)))
                    eq_parts.append(f"{build_func}(")
                    if B != 1:
                        eq_parts.append(format_number(B, 4))
                    if C != 0:
                        eq_parts.append(f"(x {'-' if C > 0 else '+'} {format_number(abs(C))})")
                    else:
                        eq_parts.append("x")
                    eq_parts.append(")")
                    if D != 0:
                        eq_parts.append(f" {'+' if D > 0 else '-'} {format_number(abs(D))}")
                    
                    equation = "".join(eq_parts)
                    
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.markdown(f'<div class="result-value">{equation}</div>', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Amplitude", format_number(abs(A)))
                        st.metric("Period", format_number(period))
                    with col2:
                        st.metric("Phase Shift", format_number(C))
                        st.metric("Vertical Shift", format_number(D))
                    
                    st.markdown('</div>', unsafe_allow_html=True)
        
        else:  # Real-World Model
            st.markdown('<div class="section-header">🌊 Real-World Sinusoidal Model</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                model_max = st.text_input("Maximum Value", placeholder="e.g., 100", key="model_max")
                model_min = st.text_input("Minimum Value", placeholder="e.g., 20", key="model_min")
            with col2:
                model_period = st.text_input("Period", placeholder="e.g., 12", key="model_period")
                model_max_time = st.text_input("Time of Maximum", placeholder="e.g., 3", key="model_max_time")
            
            if st.button("Build Model", key="build_model"):
                max_val = parse_number(model_max)
                min_val = parse_number(model_min)
                period = parse_number(model_period)
                max_time = parse_number(model_max_time)
                
                if any(math.isnan(x) for x in [max_val, min_val, period, max_time]):
                    st.error("Please enter all values.")
                elif max_val <= min_val:
                    st.error("Maximum must be greater than minimum.")
                else:
                    A = (max_val - min_val) / 2
                    D = (max_val + min_val) / 2
                    B = 2 * PI / period
                    
                    equation = f"y = {format_number(A)}cos({format_number(B, 4)}(x - {max_time})) + {format_number(D)}"
                    
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    st.markdown(f'<div class="result-value">{equation}</div>', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Amplitude", format_number(A))
                        st.metric("Period", format_number(period))
                    with col2:
                        st.metric("Phase Shift", format_number(max_time))
                        st.metric("Midline", f"y = {format_number(D)}")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
    
    # ==================== TAB 5: OBLIQUE TRIANGLES ====================
    with tab5:
        section = st.radio(
            "Select Section",
            ["Triangle Solver", "Area Calculator"],
            horizontal=True,
            key="oblique_section"
        )
        
        if section == "Triangle Solver":
            st.markdown('<div class="section-header">📐 Oblique Triangle Solver</div>', unsafe_allow_html=True)
            
            case = st.selectbox(
                "Select Case",
                ["AAS (Angle-Angle-Side)", "ASA (Angle-Side-Angle)", "SSA (Side-Side-Angle)", "SAS (Side-Angle-Side)", "SSS (Side-Side-Side)"],
                key="oblique_case"
            )
            
            case_type = case.split()[0]
            
            if case_type == "AAS":
                col1, col2, col3 = st.columns(3)
                with col1:
                    obl_A = st.text_input("Angle A (degrees)", key="obl_A_aas")
                with col2:
                    obl_B = st.text_input("Angle B (degrees)", key="obl_B_aas")
                with col3:
                    obl_a = st.text_input("Side a (opposite A)", key="obl_a_aas")
            
            elif case_type == "ASA":
                col1, col2, col3 = st.columns(3)
                with col1:
                    obl_A = st.text_input("Angle A (degrees)", key="obl_A_asa")
                with col2:
                    obl_c = st.text_input("Side c (between A and B)", key="obl_c_asa")
                with col3:
                    obl_B = st.text_input("Angle B (degrees)", key="obl_B_asa")
            
            elif case_type == "SSA":
                col1, col2, col3 = st.columns(3)
                with col1:
                    obl_a = st.text_input("Side a", key="obl_a_ssa")
                with col2:
                    obl_b = st.text_input("Side b", key="obl_b_ssa")
                with col3:
                    obl_A = st.text_input("Angle A (opposite a, degrees)", key="obl_A_ssa")
            
            elif case_type == "SAS":
                col1, col2, col3 = st.columns(3)
                with col1:
                    obl_a = st.text_input("Side a", key="obl_a_sas")
                with col2:
                    obl_C = st.text_input("Angle C (between a and b, degrees)", key="obl_C_sas")
                with col3:
                    obl_b = st.text_input("Side b", key="obl_b_sas")
            
            else:  # SSS
                col1, col2, col3 = st.columns(3)
                with col1:
                    obl_a = st.text_input("Side a", key="obl_a_sss")
                with col2:
                    obl_b = st.text_input("Side b", key="obl_b_sss")
                with col3:
                    obl_c = st.text_input("Side c", key="obl_c_sss")
            
            if st.button("Solve Triangle", key="solve_oblique"):
                try:
                    a, b, c, A, B, C = [None] * 6
                    
                    if case_type == "AAS":
                        A = parse_number(obl_A)
                        B = parse_number(obl_B)
                        a = parse_number(obl_a)
                        
                        if any(math.isnan(x) for x in [A, B, a]):
                            st.error("Please enter all values.")
                        elif A + B >= 180:
                            st.error("Angles A + B must be less than 180°")
                        else:
                            C = 180 - A - B
                            ratio = a / math.sin(to_radians(A))
                            b = ratio * math.sin(to_radians(B))
                            c = ratio * math.sin(to_radians(C))
                    
                    elif case_type == "ASA":
                        A = parse_number(obl_A)
                        B = parse_number(obl_B)
                        c = parse_number(obl_c)
                        
                        if any(math.isnan(x) for x in [A, B, c]):
                            st.error("Please enter all values.")
                        elif A + B >= 180:
                            st.error("Angles A + B must be less than 180°")
                        else:
                            C = 180 - A - B
                            ratio = c / math.sin(to_radians(C))
                            a = ratio * math.sin(to_radians(A))
                            b = ratio * math.sin(to_radians(B))
                    
                    elif case_type == "SSA":
                        a = parse_number(obl_a)
                        b = parse_number(obl_b)
                        A = parse_number(obl_A)
                        
                        if any(math.isnan(x) for x in [a, b, A]):
                            st.error("Please enter all values.")
                        else:
                            sin_B = b * math.sin(to_radians(A)) / a
                            if sin_B > 1:
                                st.error("No solution exists (sin B > 1)")
                            else:
                                B = to_degrees(math.asin(sin_B))
                                C = 180 - A - B
                                if C <= 0:
                                    st.error("No valid triangle (angles sum exceeds 180°)")
                                else:
                                    c = a * math.sin(to_radians(C)) / math.sin(to_radians(A))
                                    # Check for second solution (ambiguous case)
                                    B2 = 180 - B
                                    C2 = 180 - A - B2
                                    if C2 > 0 and B2 != B:
                                        st.warning(f"⚠️ Ambiguous case: Second solution exists with B = {format_number(B2)}°, C = {format_number(C2)}°")
                    
                    elif case_type == "SAS":
                        a = parse_number(obl_a)
                        b = parse_number(obl_b)
                        C = parse_number(obl_C)
                        
                        if any(math.isnan(x) for x in [a, b, C]):
                            st.error("Please enter all values.")
                        else:
                            c = math.sqrt(a*a + b*b - 2*a*b*math.cos(to_radians(C)))
                            if c < 1e-10:
                                st.error("Invalid triangle configuration")
                            else:
                                cos_A = max(-1, min(1, (b*b + c*c - a*a) / (2*b*c)))
                                A = to_degrees(math.acos(cos_A))
                                B = 180 - A - C
                    
                    else:  # SSS
                        a = parse_number(obl_a)
                        b = parse_number(obl_b)
                        c = parse_number(obl_c)
                        
                        if any(math.isnan(x) for x in [a, b, c]):
                            st.error("Please enter all values.")
                        elif a + b <= c or a + c <= b or b + c <= a:
                            st.error("Invalid triangle: sum of any two sides must be greater than the third")
                        else:
                            cos_A = max(-1, min(1, (b*b + c*c - a*a) / (2*b*c)))
                            cos_B = max(-1, min(1, (a*a + c*c - b*b) / (2*a*c)))
                            A = to_degrees(math.acos(cos_A))
                            B = to_degrees(math.acos(cos_B))
                            C = 180 - A - B
                    
                    if all(x is not None for x in [a, b, c, A, B, C]):
                        # Calculate area using Heron's formula
                        s = (a + b + c) / 2
                        area = math.sqrt(s * (s-a) * (s-b) * (s-c))
                        
                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Side a", format_number(a))
                            st.metric("Angle A", f"{format_number(A)}°")
                        with col2:
                            st.metric("Side b", format_number(b))
                            st.metric("Angle B", f"{format_number(B)}°")
                        with col3:
                            st.metric("Side c", format_number(c))
                            st.metric("Angle C", f"{format_number(C)}°")
                        
                        st.metric("Area", f"{format_number(area)} sq units")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        else:  # Area Calculator
            st.markdown('<div class="section-header">📏 Area Calculator</div>', unsafe_allow_html=True)
            
            area_method = st.selectbox(
                "Method",
                ["Two Sides and Included Angle (SAS)", "Heron's Formula (SSS)"],
                key="area_method"
            )
            
            if "SAS" in area_method:
                col1, col2, col3 = st.columns(3)
                with col1:
                    area_a = st.text_input("Side a", key="area_a_sas")
                with col2:
                    area_b = st.text_input("Side b", key="area_b_sas")
                with col3:
                    area_C = st.text_input("Included Angle C (degrees)", key="area_C_sas")
                
                if st.button("Calculate Area", key="calc_area_sas"):
                    a = parse_number(area_a)
                    b = parse_number(area_b)
                    C = parse_number(area_C)
                    
                    if any(math.isnan(x) for x in [a, b, C]):
                        st.error("Please enter all values.")
                    else:
                        area = 0.5 * a * b * math.sin(to_radians(C))
                        
                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        st.metric("Area", f"{format_number(area)} sq units")
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        if show_steps:
                            steps = f"""Area using SAS Formula

Given:
  Side a = {a}
  Side b = {b}
  Angle C = {C}°

Formula: Area = ½ × a × b × sin(C)

Calculation:
  Area = ½ × {a} × {b} × sin({C}°)
  Area = ½ × {a} × {b} × {format_number(math.sin(to_radians(C)))}
  Area = {format_number(area)} square units"""
                            st.markdown(f'<div class="steps-box">{steps}</div>', unsafe_allow_html=True)
            
            else:  # Heron's Formula
                col1, col2, col3 = st.columns(3)
                with col1:
                    area_a = st.text_input("Side a", key="area_a_sss")
                with col2:
                    area_b = st.text_input("Side b", key="area_b_sss")
                with col3:
                    area_c = st.text_input("Side c", key="area_c_sss")
                
                if st.button("Calculate Area", key="calc_area_sss"):
                    a = parse_number(area_a)
                    b = parse_number(area_b)
                    c = parse_number(area_c)
                    
                    if any(math.isnan(x) for x in [a, b, c]):
                        st.error("Please enter all values.")
                    elif a + b <= c or a + c <= b or b + c <= a:
                        st.error("Invalid triangle")
                    else:
                        s = (a + b + c) / 2
                        area = math.sqrt(s * (s-a) * (s-b) * (s-c))
                        
                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        st.metric("Area", f"{format_number(area)} sq units")
                        st.metric("Semi-perimeter (s)", format_number(s))
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        if show_steps:
                            steps = f"""Area using Heron's Formula

Given:
  Side a = {a}
  Side b = {b}
  Side c = {c}

Step 1: Calculate semi-perimeter
  s = (a + b + c) / 2
  s = ({a} + {b} + {c}) / 2
  s = {format_number(s)}

Step 2: Apply Heron's formula
  Area = √(s(s-a)(s-b)(s-c))
  Area = √({format_number(s)} × {format_number(s-a)} × {format_number(s-b)} × {format_number(s-c)})
  Area = √{format_number(s * (s-a) * (s-b) * (s-c))}
  Area = {format_number(area)} square units"""
                            st.markdown(f'<div class="steps-box">{steps}</div>', unsafe_allow_html=True)

# ============================================================
# ADVANCED CALCULATOR
# ============================================================

else:  # Advanced
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Trig Equations",
        "🎯 Vectors",
        "🔄 Polar & Complex",
        "📈 Parametric & Motion"
    ])
    
    # ==================== TAB 1: TRIG EQUATIONS ====================
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="section-header">Basic Trig Functions</div>', unsafe_allow_html=True)
            
            basic_func = st.selectbox("Function", ["sin(θ)", "cos(θ)", "tan(θ)", "csc(θ)", "sec(θ)", "cot(θ)"], key="adv_basic_func")
            basic_angle = st.text_input("Angle (θ)", placeholder="Enter angle", key="adv_basic_angle")
            
            if st.button("Calculate", key="calc_basic_adv"):
                if basic_angle:
                    try:
                        angle_val = parse_number(basic_angle)
                        
                        if math.isnan(angle_val):
                            st.error("Invalid angle.")
                        else:
                            angle_rad = angle_val if use_radians else to_radians(angle_val)
                            func_name = basic_func.split('(')[0]
                            
                            if func_name == 'sin':
                                result = math.sin(angle_rad)
                            elif func_name == 'cos':
                                result = math.cos(angle_rad)
                            elif func_name == 'tan':
                                if abs(math.cos(angle_rad)) < 1e-10:
                                    st.error("Undefined (cos = 0)")
                                    result = None
                                else:
                                    result = math.tan(angle_rad)
                            elif func_name == 'csc':
                                if abs(math.sin(angle_rad)) < 1e-10:
                                    st.error("Undefined (sin = 0)")
                                    result = None
                                else:
                                    result = 1 / math.sin(angle_rad)
                            elif func_name == 'sec':
                                if abs(math.cos(angle_rad)) < 1e-10:
                                    st.error("Undefined (cos = 0)")
                                    result = None
                                else:
                                    result = 1 / math.cos(angle_rad)
                            else:  # cot
                                if abs(math.sin(angle_rad)) < 1e-10:
                                    st.error("Undefined (sin = 0)")
                                    result = None
                                else:
                                    result = 1 / math.tan(angle_rad)
                            
                            if result is not None:
                                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                                st.metric("Result", format_number(result, 10))
                                st.markdown('</div>', unsafe_allow_html=True)
                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        with col2:
            st.markdown('<div class="section-header">Inverse Trig Functions</div>', unsafe_allow_html=True)
            
            inv_func = st.selectbox("Function", ["arcsin(x)", "arccos(x)", "arctan(x)", "arccsc(x)", "arcsec(x)", "arccot(x)"], key="adv_inv_func")
            inv_value = st.text_input("Value (x)", placeholder="Enter value", key="adv_inv_value")
            
            if st.button("Calculate", key="calc_inv_adv"):
                if inv_value:
                    try:
                        x = parse_number(inv_value)
                        
                        if math.isnan(x):
                            st.error("Invalid value.")
                        else:
                            func_name = inv_func.split('(')[0]
                            result = None
                            
                            if func_name == 'arcsin':
                                if x < -1 or x > 1:
                                    st.error("Value must be in [-1, 1]")
                                else:
                                    result = math.asin(x)
                            elif func_name == 'arccos':
                                if x < -1 or x > 1:
                                    st.error("Value must be in [-1, 1]")
                                else:
                                    result = math.acos(x)
                            elif func_name == 'arctan':
                                result = math.atan(x)
                            elif func_name == 'arccsc':
                                if -1 < x < 1:
                                    st.error("|x| must be ≥ 1")
                                else:
                                    result = math.asin(1/x)
                            elif func_name == 'arcsec':
                                if -1 < x < 1:
                                    st.error("|x| must be ≥ 1")
                                else:
                                    result = math.acos(1/x)
                            else:  # arccot
                                result = math.atan(1/x)
                                if x < 0:
                                    result += PI
                            
                            if result is not None:
                                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                                if use_radians:
                                    st.metric("Result", f"{format_number(result)} rad")
                                else:
                                    st.metric("Result", f"{format_number(to_degrees(result))}°")
                                st.markdown('</div>', unsafe_allow_html=True)
                    
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
        
        st.markdown("---")
        st.markdown('<div class="section-header">Solve Trig Equation</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            eq_type = st.selectbox(
                "Equation Type",
                ["sin(θ) = k", "cos(θ) = k", "tan(θ) = k"],
                key="eq_type"
            )
        with col2:
            eq_k = st.text_input("Value of k", placeholder="e.g., 0.5", key="eq_k")
        
        if st.button("Solve", key="solve_eq"):
            if eq_k:
                try:
                    k = parse_number(eq_k)
                    
                    if math.isnan(k):
                        st.error("Invalid value.")
                    else:
                        if "sin" in eq_type:
                            if k < -1 or k > 1:
                                st.error("No solution: sin(θ) ∈ [-1, 1]")
                            else:
                                base = to_degrees(math.asin(k))
                                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                                st.markdown(f"**Solutions:**")
                                st.markdown(f"θ = {format_number(base)}° + 360°n")
                                st.markdown(f"θ = {format_number(180 - base)}° + 360°n")
                                st.markdown("where n is any integer")
                                st.markdown('</div>', unsafe_allow_html=True)
                        
                        elif "cos" in eq_type:
                            if k < -1 or k > 1:
                                st.error("No solution: cos(θ) ∈ [-1, 1]")
                            else:
                                base = to_degrees(math.acos(k))
                                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                                st.markdown(f"**Solutions:**")
                                st.markdown(f"θ = ±{format_number(base)}° + 360°n")
                                st.markdown("where n is any integer")
                                st.markdown('</div>', unsafe_allow_html=True)
                        
                        else:  # tan
                            base = to_degrees(math.atan(k))
                            st.markdown('<div class="result-box">', unsafe_allow_html=True)
                            st.markdown(f"**Solutions:**")
                            st.markdown(f"θ = {format_number(base)}° + 180°n")
                            st.markdown("where n is any integer")
                            st.markdown('</div>', unsafe_allow_html=True)
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    # ==================== TAB 2: VECTORS ====================
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="section-header">Vector Operations</div>', unsafe_allow_html=True)
            
            vec_col1, vec_col2 = st.columns(2)
            with vec_col1:
                st.markdown("**Vector U**")
                ux = st.text_input("Uₓ", placeholder="e.g., 3", key="ux")
                uy = st.text_input("Uᵧ", placeholder="e.g., 4", key="uy")
            with vec_col2:
                st.markdown("**Vector V**")
                vx = st.text_input("Vₓ", placeholder="e.g., 1", key="vx")
                vy = st.text_input("Vᵧ", placeholder="e.g., 2", key="vy")
            
            vec_op = st.selectbox(
                "Operation",
                ["Add (U + V)", "Subtract (U - V)", "Dot Product (U · V)", "Cross Product (U × V)", "Angle Between"],
                key="vec_op"
            )
            
            if st.button("Calculate", key="calc_vec"):
                try:
                    u_x = parse_number(ux)
                    u_y = parse_number(uy)
                    v_x = parse_number(vx)
                    v_y = parse_number(vy)
                    
                    if any(math.isnan(x) for x in [u_x, u_y, v_x, v_y]):
                        st.error("Please enter all vector components.")
                    else:
                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        
                        if "Add" in vec_op:
                            rx, ry = u_x + v_x, u_y + v_y
                            st.metric("Result", f"({format_number(rx)}, {format_number(ry)})")
                            st.metric("Magnitude", format_number(math.sqrt(rx*rx + ry*ry)))
                        
                        elif "Subtract" in vec_op:
                            rx, ry = u_x - v_x, u_y - v_y
                            st.metric("Result", f"({format_number(rx)}, {format_number(ry)})")
                            st.metric("Magnitude", format_number(math.sqrt(rx*rx + ry*ry)))
                        
                        elif "Dot" in vec_op:
                            dot = u_x * v_x + u_y * v_y
                            st.metric("U · V", format_number(dot))
                            st.info("Dot product is 0 if vectors are perpendicular")
                        
                        elif "Cross" in vec_op:
                            cross = u_x * v_y - u_y * v_x
                            st.metric("U × V (z-component)", format_number(cross))
                            st.info("This represents the signed area of the parallelogram")
                        
                        else:  # Angle
                            mag_u = math.sqrt(u_x*u_x + u_y*u_y)
                            mag_v = math.sqrt(v_x*v_x + v_y*v_y)
                            if mag_u < 1e-10 or mag_v < 1e-10:
                                st.error("Cannot find angle with zero vector")
                            else:
                                dot = u_x * v_x + u_y * v_y
                                cos_angle = max(-1, min(1, dot / (mag_u * mag_v)))  # Clamp to [-1, 1]
                                angle = math.acos(cos_angle)
                                if use_radians:
                                    st.metric("Angle", f"{format_number(angle)} rad")
                                else:
                                    st.metric("Angle", f"{format_number(to_degrees(angle))}°")
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        with col2:
            st.markdown('<div class="section-header">Single Vector Properties</div>', unsafe_allow_html=True)
            
            sv_x = st.text_input("x-component", placeholder="e.g., 3", key="sv_x")
            sv_y = st.text_input("y-component", placeholder="e.g., 4", key="sv_y")
            
            if st.button("Analyze", key="analyze_vec"):
                try:
                    x = parse_number(sv_x)
                    y = parse_number(sv_y)
                    
                    if math.isnan(x) or math.isnan(y):
                        st.error("Please enter both components.")
                    else:
                        magnitude = math.sqrt(x*x + y*y)
                        direction = math.atan2(y, x)
                        
                        if magnitude > 1e-10:
                            unit_x = x / magnitude
                            unit_y = y / magnitude
                        else:
                            unit_x = unit_y = 0
                        
                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        st.metric("Magnitude", format_number(magnitude))
                        if use_radians:
                            st.metric("Direction", f"{format_number(direction)} rad")
                        else:
                            st.metric("Direction", f"{format_number(to_degrees(direction))}°")
                        st.metric("Unit Vector", f"({format_number(unit_x)}, {format_number(unit_y)})")
                        st.markdown('</div>', unsafe_allow_html=True)
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    # ==================== TAB 3: POLAR & COMPLEX ====================
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="section-header">Rectangular ↔ Polar Conversion</div>', unsafe_allow_html=True)
            
            conv_dir = st.radio("Conversion", ["Rectangular → Polar", "Polar → Rectangular"], key="polar_conv_dir")
            
            if "Rectangular → Polar" in conv_dir:
                polar_x = st.text_input("x", placeholder="e.g., 3", key="polar_x")
                polar_y = st.text_input("y", placeholder="e.g., 4", key="polar_y")
                
                if st.button("Convert", key="conv_to_polar"):
                    x = parse_number(polar_x)
                    y = parse_number(polar_y)
                    
                    if math.isnan(x) or math.isnan(y):
                        st.error("Please enter both values.")
                    else:
                        r = math.sqrt(x*x + y*y)
                        theta = math.atan2(y, x)
                        
                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        st.metric("r", format_number(r))
                        if use_radians:
                            st.metric("θ", f"{format_number(theta)} rad")
                        else:
                            st.metric("θ", f"{format_number(to_degrees(theta))}°")
                        st.markdown('</div>', unsafe_allow_html=True)
            else:
                polar_r = st.text_input("r", placeholder="e.g., 5", key="polar_r")
                angle_label = "radians" if use_radians else "degrees"
                polar_theta = st.text_input(f"θ ({angle_label})", placeholder="e.g., 45", key="polar_theta")
                
                if st.button("Convert", key="conv_to_rect"):
                    r = parse_number(polar_r)
                    theta = parse_number(polar_theta)
                    
                    if math.isnan(r) or math.isnan(theta):
                        st.error("Please enter both values.")
                    else:
                        theta_rad = theta if use_radians else to_radians(theta)
                        x = r * math.cos(theta_rad)
                        y = r * math.sin(theta_rad)
                        
                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        st.metric("x", format_number(x))
                        st.metric("y", format_number(y))
                        st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="section-header">Complex Number Operations</div>', unsafe_allow_html=True)
            
            z1_col, z2_col = st.columns(2)
            with z1_col:
                st.markdown("**Z₁ = a + bi**")
                z1_real = st.text_input("a (real)", placeholder="e.g., 3", key="z1_real")
                z1_imag = st.text_input("b (imag)", placeholder="e.g., 4", key="z1_imag")
            with z2_col:
                st.markdown("**Z₂ = c + di**")
                z2_real = st.text_input("c (real)", placeholder="e.g., 1", key="z2_real")
                z2_imag = st.text_input("d (imag)", placeholder="e.g., 2", key="z2_imag")
            
            complex_op = st.selectbox(
                "Operation",
                ["Add (Z₁ + Z₂)", "Subtract (Z₁ - Z₂)", "Multiply (Z₁ × Z₂)", "Divide (Z₁ ÷ Z₂)", "Modulus |Z₁|", "Conjugate Z̄₁", "To Polar Form"],
                key="complex_op"
            )
            
            if st.button("Calculate", key="calc_complex"):
                try:
                    a = parse_number(z1_real)
                    b = parse_number(z1_imag)
                    
                    if math.isnan(a) or math.isnan(b):
                        st.error("Please enter Z₁.")
                    else:
                        need_z2 = any(op in complex_op for op in ["Add", "Subtract", "Multiply", "Divide"])
                        
                        if need_z2:
                            c = parse_number(z2_real)
                            d = parse_number(z2_imag)
                            if math.isnan(c) or math.isnan(d):
                                st.error("Please enter Z₂.")
                                c = d = None
                        else:
                            c = d = 0
                        
                        if c is not None:
                            st.markdown('<div class="result-box">', unsafe_allow_html=True)
                            
                            if "Add" in complex_op:
                                st.metric("Result", format_complex(a+c, b+d))
                            elif "Subtract" in complex_op:
                                st.metric("Result", format_complex(a-c, b-d))
                            elif "Multiply" in complex_op:
                                re = a*c - b*d
                                im = a*d + b*c
                                st.metric("Result", format_complex(re, im))
                            elif "Divide" in complex_op:
                                denom = c*c + d*d
                                if denom < 1e-10:
                                    st.error("Cannot divide by zero")
                                else:
                                    re = (a*c + b*d) / denom
                                    im = (b*c - a*d) / denom
                                    st.metric("Result", format_complex(re, im))
                            elif "Modulus" in complex_op:
                                st.metric("|Z₁|", format_number(math.sqrt(a*a + b*b)))
                            elif "Conjugate" in complex_op:
                                st.metric("Z̄₁", format_complex(a, -b))
                            else:  # Polar
                                r = math.sqrt(a*a + b*b)
                                theta = math.atan2(b, a)
                                theta_str = f"{format_number(theta)} rad" if use_radians else f"{format_number(to_degrees(theta))}°"
                                st.metric("r", format_number(r))
                                st.metric("θ", theta_str)
                                st.markdown(f"**Polar form:** {format_number(r)}(cos({theta_str}) + i·sin({theta_str}))")
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                
                except Exception as e:
                    st.error(f"Error: {str(e)}")
        
        st.markdown("---")
        st.markdown('<div class="section-header">De Moivre\'s Theorem</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            angle_label = "radians" if use_radians else "degrees"
            dm_theta = st.text_input(f"Angle θ ({angle_label})", placeholder="e.g., 30", key="dm_theta")
        with col2:
            dm_n = st.text_input("Power n", placeholder="e.g., 3", key="dm_n")
        
        if st.button("Apply De Moivre's Theorem", key="calc_demoivre"):
            theta = parse_number(dm_theta)
            n = parse_number(dm_n)
            
            if math.isnan(theta) or math.isnan(n):
                st.error("Please enter both values.")
            else:
                theta_rad = theta if use_radians else to_radians(theta)
                new_theta = n * theta_rad
                cos_result = math.cos(new_theta)
                sin_result = math.sin(new_theta)
                
                st.markdown('<div class="result-box">', unsafe_allow_html=True)
                st.markdown(f"**(cos θ + i·sin θ)ⁿ = cos(nθ) + i·sin(nθ)**")
                st.metric("Result", format_complex(cos_result, sin_result))
                st.markdown('</div>', unsafe_allow_html=True)
    
    # ==================== TAB 4: PARAMETRIC & MOTION ====================
    with tab4:
        section = st.radio(
            "Select Section",
            ["Parametric Equations", "Projectile Motion", "Simple Harmonic Motion"],
            horizontal=True,
            key="motion_section"
        )
        
        if section == "Parametric Equations":
            st.markdown('<div class="section-header">Parametric Equations</div>', unsafe_allow_html=True)
            
            curve_type = st.selectbox(
                "Curve Type",
                ["Circle", "Ellipse", "Cycloid", "Lissajous"],
                key="curve_type"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                param_t = st.text_input("Parameter t", placeholder="e.g., π/4", key="param_t")
                
                if curve_type == "Circle":
                    param_r = st.text_input("Radius r", placeholder="e.g., 5", key="param_r")
                elif curve_type == "Ellipse":
                    param_a = st.text_input("Semi-major axis a", placeholder="e.g., 5", key="param_ea")
                    param_b = st.text_input("Semi-minor axis b", placeholder="e.g., 3", key="param_eb")
                elif curve_type == "Cycloid":
                    param_r = st.text_input("Rolling radius r", placeholder="e.g., 5", key="param_cr")
            
            if st.button("Calculate Point", key="calc_param"):
                t = parse_number(param_t)
                
                if math.isnan(t):
                    st.error("Please enter parameter t.")
                else:
                    x = y = None
                    
                    if curve_type == "Circle":
                        r = parse_number(param_r) if param_r else 5
                        x = r * math.cos(t)
                        y = r * math.sin(t)
                        st.info(f"Equations: x(t) = r·cos(t), y(t) = r·sin(t)")
                    
                    elif curve_type == "Ellipse":
                        a = parse_number(param_a) if param_a else 5
                        b = parse_number(param_b) if param_b else 3
                        x = a * math.cos(t)
                        y = b * math.sin(t)
                        st.info(f"Equations: x(t) = a·cos(t), y(t) = b·sin(t)")
                    
                    elif curve_type == "Cycloid":
                        r = parse_number(param_r) if param_r else 5
                        x = r * (t - math.sin(t))
                        y = r * (1 - math.cos(t))
                        st.info(f"Equations: x(t) = r(t - sin(t)), y(t) = r(1 - cos(t))")
                    
                    if x is not None:
                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        col1, col2 = st.columns(2)
                        with col1:
                            st.metric("x(t)", format_number(x))
                        with col2:
                            st.metric("y(t)", format_number(y))
                        st.markdown('</div>', unsafe_allow_html=True)
        
        elif section == "Projectile Motion":
            st.markdown('<div class="section-header">Projectile Motion</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                proj_v0 = st.text_input("Initial Velocity (m/s)", placeholder="e.g., 50", key="proj_v0")
                proj_angle = st.text_input("Launch Angle (degrees)", placeholder="e.g., 45", key="proj_angle")
            with col2:
                proj_h0 = st.text_input("Initial Height (m)", placeholder="e.g., 0", value="0", key="proj_h0")
                proj_g = st.text_input("Gravity (m/s²)", placeholder="e.g., 9.81", value="9.81", key="proj_g")
            
            if st.button("Analyze Projectile", key="calc_proj"):
                v0 = parse_number(proj_v0)
                angle = parse_number(proj_angle)
                h0 = parse_number(proj_h0)
                g = parse_number(proj_g)
                
                if any(math.isnan(x) for x in [v0, angle]):
                    st.error("Please enter velocity and angle.")
                else:
                    angle_rad = to_radians(angle)
                    v0x = v0 * math.cos(angle_rad)
                    v0y = v0 * math.sin(angle_rad)
                    
                    t_max = v0y / g
                    max_height = h0 + (v0y * v0y) / (2 * g)
                    
                    discriminant = v0y * v0y + 2 * g * h0
                    total_time = (v0y + math.sqrt(discriminant)) / g
                    range_dist = v0x * total_time
                    
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Maximum Height", f"{format_number(max_height)} m")
                        st.metric("Horizontal Velocity", f"{format_number(v0x)} m/s")
                    with col2:
                        st.metric("Range", f"{format_number(range_dist)} m")
                        st.metric("Vertical Velocity", f"{format_number(v0y)} m/s")
                    with col3:
                        st.metric("Time of Flight", f"{format_number(total_time)} s")
                        st.metric("Time to Max Height", f"{format_number(t_max)} s")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    if show_steps:
                        steps = f"""Projectile Motion Analysis

Given:
  Initial velocity v₀ = {v0} m/s
  Launch angle θ = {angle}°
  Initial height h₀ = {h0} m
  Gravity g = {g} m/s²

Step 1: Calculate velocity components
  v₀ₓ = v₀ × cos(θ) = {v0} × cos({angle}°) = {format_number(v0x)} m/s
  v₀ᵧ = v₀ × sin(θ) = {v0} × sin({angle}°) = {format_number(v0y)} m/s

Step 2: Calculate time to maximum height
  t_max = v₀ᵧ/g = {format_number(v0y)}/{g} = {format_number(t_max)} s

Step 3: Calculate maximum height
  H_max = h₀ + v₀ᵧ²/(2g) = {h0} + {format_number(v0y*v0y/(2*g))} = {format_number(max_height)} m

Step 4: Calculate total time of flight
  t = (v₀ᵧ + √(v₀ᵧ² + 2gh₀))/g = {format_number(total_time)} s

Step 5: Calculate range
  R = v₀ₓ × t = {format_number(v0x)} × {format_number(total_time)} = {format_number(range_dist)} m"""
                        st.markdown(f'<div class="steps-box">{steps}</div>', unsafe_allow_html=True)
        
        else:  # Simple Harmonic Motion
            st.markdown('<div class="section-header">Simple Harmonic Motion</div>', unsafe_allow_html=True)
            st.info("Equation: x(t) = A·cos(ωt + φ)")
            
            col1, col2 = st.columns(2)
            with col1:
                shm_A = st.text_input("Amplitude A", placeholder="e.g., 5", key="shm_A")
                shm_omega = st.text_input("Angular Frequency ω (rad/s)", placeholder="e.g., 2", key="shm_omega")
            with col2:
                shm_phi = st.text_input("Initial Phase φ (rad)", placeholder="e.g., 0", value="0", key="shm_phi")
                shm_t = st.text_input("Time t (s)", placeholder="e.g., 1", key="shm_t")
            
            if st.button("Calculate", key="calc_shm"):
                A = parse_number(shm_A)
                omega = parse_number(shm_omega)
                phi = parse_number(shm_phi)
                t = parse_number(shm_t)
                
                if any(math.isnan(x) for x in [A, omega, t]):
                    st.error("Please enter A, ω, and t.")
                else:
                    position = A * math.cos(omega * t + phi)
                    velocity = -A * omega * math.sin(omega * t + phi)
                    acceleration = -A * omega * omega * math.cos(omega * t + phi)
                    period = 2 * PI / omega
                    frequency = omega / (2 * PI)
                    
                    st.markdown('<div class="result-box">', unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Position x(t)", format_number(position))
                        st.metric("Period T", f"{format_number(period)} s")
                    with col2:
                        st.metric("Velocity v(t)", format_number(velocity))
                        st.metric("Frequency f", f"{format_number(frequency)} Hz")
                    with col3:
                        st.metric("Acceleration a(t)", format_number(acceleration))
                        st.metric("Max Velocity", format_number(A * omega))
                    
                    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 14px;">
    📐 Trigonometry Calculator | Built with Streamlit
</div>
""", unsafe_allow_html=True)
