import math

def get_gear_ratio(x, v, slope, mu, track_info):
    """
    // Code by Tamal Krishna Chhabra (AUP)
    Eco-Gear Controller Logic in short:
    - Optimization: Balances theoretical efficiency with real time physics constraints.
    - Efficient Cruising: targets speed where aerodynamic drag equals rolling resistance.
    - Traction Control: Limits gear based on friction (mu) and normal force to prevent slip.
    - Anticipation: Look-ahead (40m) sprints for steep climbs and brakes for icy zones.
    - Stall Prevention: Precise 'soft start' logic ensures enough torque to overcome gravity on hills.
    - Momentum Management: Uses 'Pulse and Glide' on flats and coasting on downhills to save fuel.
    """
    
    # Physics constants
    # Fixed environmental and vehicle parameters used in force calculations
    MASS = 70.0
    GRAVITY = 9.81
    WHEEL_RADIUS = 0.35
    MAX_TORQUE = 100.0
    DRAG_COEFF = 0.9
    FRONTAL_AREA = 0.5
    AIR_DENSITY = 1.2
    ROLLING_RESISTANCE = 0.01
    
    AERO_FACTOR = 0.5 * AIR_DENSITY * DRAG_COEFF * FRONTAL_AREA

    # Controller settings
    # Tunable parameters that define safety margins, lookahead distance, and strategic thresholds
    TRACTION_SAFETY_FACTOR = 0.70
    LOOKAHEAD_DISTANCE = 40.0
    DANGER_SLOPE_THRESHOLD = 0.11
    LOW_MU_THRESHOLD = 0.5
    FINISH_COAST_DISTANCE = 45.0
    MIN_COAST_SPEED = 4.0

    PNG_SPEED_TOLERANCE = 1.0
    PNG_BURST_ACCEL = 0.8

    UPHILL_LAUNCH_MARGIN = 1.2
    FLAT_LAUNCH_RAMP = 0.3

    # Update physics state
    # Decomposes slope into angle components and calculates acting forces (Gravity, Normal, Rolling)
    theta = math.atan(slope)
    sin_theta = math.sin(theta)
    cos_theta = math.cos(theta)
    
    gravity_force = MASS * GRAVITY * sin_theta
    normal_force = MASS * GRAVITY * cos_theta
    current_rolling_resist = ROLLING_RESISTANCE * normal_force
    
    # Calculate traction limit
    # Determines the maximum torque the tires can transmit before slipping based on friction (mu)
    max_traction_force = mu * normal_force
    
    current_safety_factor = TRACTION_SAFETY_FACTOR
    if mu < LOW_MU_THRESHOLD:
        current_safety_factor = 0.25
        
    traction_limited_gear = (max_traction_force * current_safety_factor * WHEEL_RADIUS) / MAX_TORQUE
    
    # Calculate gravity hold
    # Computes the minimum torque required to prevent the rover from rolling backwards on an uphill
    if slope > 0:
        gravity_hold_gear = (gravity_force * WHEEL_RADIUS) / MAX_TORQUE
    else:
        gravity_hold_gear = 0.0

    # Calculate optimal speed
    # Derives the efficient cruising velocity where aerodynamic drag balances out rolling resistance
    try:
        opt_cruise_speed = math.sqrt(current_rolling_resist / AERO_FACTOR)
    except ValueError:
        opt_cruise_speed = 5.0 
        
    # Look ahead for danger
    # Scans upcoming track segments to anticipate steep climbs or low friction zones
    segments = track_info.get('segments', [])
    finish_pos = track_info.get('finish_line', float('inf'))
    
    # Adaptive Minimum Speed
    # Long tracks need higher avg speed to prevent time-out.
    # Short tracks can afford to go slower/more efficient.
    min_speed_clamp = 5.2 
    if finish_pos > 400.0:
        min_speed_clamp = 6.8

    opt_cruise_speed = max(min_speed_clamp, min(10.0, opt_cruise_speed))
    
    upcoming_steep_climb = False
    upcoming_low_traction = False
    
    for seg in segments:
        s_start, s_end, s_slope, s_mu = seg
        if s_end > x and s_start < x + LOOKAHEAD_DISTANCE:
            dist_to_seg = max(0, s_start - x)
            
            if s_slope > DANGER_SLOPE_THRESHOLD:
                upcoming_steep_climb = True
            elif s_slope > 0.08 and s_mu < 0.6:
                # Moderate slope but slippery -> Momentum needed!
                upcoming_steep_climb = True
                
            if s_mu < LOW_MU_THRESHOLD:
                if dist_to_seg < LOOKAHEAD_DISTANCE / 2:
                    upcoming_low_traction = True

    # Determine target state
    # Selects the driving mode (Coast, Sprint, Safety, Climb, or Pulse-and-Glide) based on terrain
    target_v = opt_cruise_speed
    accel_target = 0.0 
    
    dist_to_finish = finish_pos - x
    if dist_to_finish < FINISH_COAST_DISTANCE:
        if v > MIN_COAST_SPEED and slope < 0.02:
             return 0.0 
             
    if slope < -0.02: 
        if v > opt_cruise_speed:
            return 0.0
            
    if upcoming_steep_climb:
        target_v = opt_cruise_speed * 1.5 
        accel_target = 0.5 
        
    elif upcoming_low_traction:
        target_v = 3.0
        if v > target_v:
             accel_target = -0.5 
        else:
             accel_target = 0.0 
        
    elif slope > 0.05:
        grade_factor = min(1.0, slope / 0.2)
        target_v = opt_cruise_speed * (1.0 - 0.3 * grade_factor)
        
    elif abs(slope) <= 0.05 and not upcoming_low_traction:
        v_high = opt_cruise_speed + PNG_SPEED_TOLERANCE
        v_low = opt_cruise_speed - PNG_SPEED_TOLERANCE
        
        if v > v_high:
            return 0.0
        elif v < v_low:
            accel_target = PNG_BURST_ACCEL
            target_v = v_high
        else:
            if v > opt_cruise_speed:
                return 0.0
            else:
                 accel_target = PNG_BURST_ACCEL * 0.5

    # Calculate required torque
    # Uses a P-controller to determine the force needed to reach the target velocity or acceleration
    kp = 1.0
    if accel_target != 0.0:
        a_desired = accel_target
    else:
        a_desired = kp * (target_v - v)
        
    a_desired = max(-1.0, min(1.5, a_desired))
    
    estimated_drag = AERO_FACTOR * v**2
    
    total_force_needed = (MASS * a_desired) + gravity_force + estimated_drag + current_rolling_resist
    
    required_torque = total_force_needed * WHEEL_RADIUS
    raw_gear = required_torque / MAX_TORQUE
    
    # Apply safety limits
    # Clamps the final gear ratio to stay within physical traction limits and prevent stalling
    final_gear = max(0.0, min(5.0, raw_gear))
    final_gear = min(final_gear, traction_limited_gear)
    
    if v < 4.0:
        if slope >= 0.05:
            safe_launch_accel = 0.5 + (0.1 * v)
            launch_force = gravity_force + current_rolling_resist + (MASS * safe_launch_accel)
            
            launch_gear = (launch_force * WHEEL_RADIUS) / MAX_TORQUE
            launch_gear = min(launch_gear, traction_limited_gear)
            
            final_gear = min(final_gear, launch_gear)
            
        elif slope > -0.02:
            flat_limit = 0.2 + (FLAT_LAUNCH_RAMP * v)
            final_gear = min(final_gear, flat_limit * 5.0)
            
    return final_gear
