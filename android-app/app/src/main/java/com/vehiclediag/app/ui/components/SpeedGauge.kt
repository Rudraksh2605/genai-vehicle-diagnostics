package com.vehiclediag.app.ui.components

import androidx.compose.animation.core.*
import androidx.compose.foundation.Canvas
import androidx.compose.foundation.layout.*
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.geometry.Offset
import androidx.compose.ui.geometry.Size
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.drawscope.Stroke
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.vehiclediag.app.ui.theme.*
import kotlin.math.cos
import kotlin.math.sin

/**
 * SpeedGauge composable — a semicircular gauge displaying current vehicle speed.
 * Animates smoothly between speed values with color transitions.
 */
@Composable
fun SpeedGauge(
    speed: Double,
    maxSpeed: Double = 200.0,
    modifier: Modifier = Modifier
) {
    val animatedSpeed by animateFloatAsState(
        targetValue = speed.toFloat(),
        animationSpec = tween(durationMillis = 500, easing = FastOutSlowInEasing),
        label = "speed_animation"
    )

    val sweepAngle = (animatedSpeed / maxSpeed.toFloat()) * 240f
    val gaugeColor = when {
        speed > 120 -> GaugeRed
        speed > 80 -> GaugeYellow
        else -> GaugeGreen
    }

    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = modifier
    ) {
        Box(
            contentAlignment = Alignment.Center,
            modifier = Modifier.size(200.dp)
        ) {
            Canvas(modifier = Modifier.size(180.dp)) {
                val strokeWidth = 16.dp.toPx()
                val arcSize = Size(size.width - strokeWidth, size.height - strokeWidth)
                val topLeft = Offset(strokeWidth / 2, strokeWidth / 2)

                // Background arc
                drawArc(
                    color = DarkSurfaceVariant,
                    startAngle = 150f,
                    sweepAngle = 240f,
                    useCenter = false,
                    topLeft = topLeft,
                    size = arcSize,
                    style = Stroke(width = strokeWidth, cap = StrokeCap.Round)
                )

                // Value arc
                drawArc(
                    color = gaugeColor,
                    startAngle = 150f,
                    sweepAngle = sweepAngle,
                    useCenter = false,
                    topLeft = topLeft,
                    size = arcSize,
                    style = Stroke(width = strokeWidth, cap = StrokeCap.Round)
                )

                // Tick marks
                val center = Offset(size.width / 2, size.height / 2)
                val radius = (size.width - strokeWidth) / 2
                for (i in 0..8) {
                    val angle = Math.toRadians((150.0 + i * 30.0))
                    val innerRadius = radius - 10.dp.toPx()
                    val outerRadius = radius - 4.dp.toPx()
                    val start = Offset(
                        center.x + innerRadius * cos(angle).toFloat(),
                        center.y + innerRadius * sin(angle).toFloat()
                    )
                    val end = Offset(
                        center.x + outerRadius * cos(angle).toFloat(),
                        center.y + outerRadius * sin(angle).toFloat()
                    )
                    drawLine(
                        color = TextMuted,
                        start = start,
                        end = end,
                        strokeWidth = 2.dp.toPx()
                    )
                }
            }

            Column(horizontalAlignment = Alignment.CenterHorizontally) {
                Text(
                    text = "%.0f".format(animatedSpeed),
                    fontSize = 42.sp,
                    fontWeight = FontWeight.Bold,
                    color = TextPrimary
                )
                Text(
                    text = "km/h",
                    fontSize = 14.sp,
                    color = TextSecondary
                )
            }
        }

        Text(
            text = "Vehicle Speed",
            style = MaterialTheme.typography.titleMedium,
            color = TextSecondary,
            modifier = Modifier.padding(top = 4.dp)
        )
    }
}
