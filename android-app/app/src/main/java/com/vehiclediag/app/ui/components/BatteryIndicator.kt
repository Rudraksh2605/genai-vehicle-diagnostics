package com.vehiclediag.app.ui.components

import androidx.compose.animation.core.*
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.vehiclediag.app.ui.theme.*

/**
 * BatteryIndicator composable — Shows battery SoC as an animated progress bar
 * with gradient fill and health status.
 */
@Composable
fun BatteryIndicator(
    soc: Double,
    voltage: Double,
    temperature: Double,
    healthStatus: String,
    modifier: Modifier = Modifier
) {
    val animatedSoc by animateFloatAsState(
        targetValue = (soc / 100.0).toFloat().coerceIn(0f, 1f),
        animationSpec = tween(durationMillis = 500, easing = FastOutSlowInEasing),
        label = "battery_animation"
    )

    val barColor = when {
        soc < 20 -> GaugeRed
        soc < 50 -> GaugeYellow
        else -> GaugeGreen
    }

    val gradientBrush = Brush.horizontalGradient(
        colors = listOf(barColor.copy(alpha = 0.6f), barColor)
    )

    Column(
        modifier = modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .background(DarkCard)
            .padding(16.dp)
    ) {
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(
                text = "🔋 Battery",
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.SemiBold,
                color = TextPrimary
            )
            Text(
                text = "%.1f%%".format(soc),
                fontSize = 24.sp,
                fontWeight = FontWeight.Bold,
                color = barColor
            )
        }

        Spacer(modifier = Modifier.height(12.dp))

        // Progress bar
        Box(
            modifier = Modifier
                .fillMaxWidth()
                .height(12.dp)
                .clip(RoundedCornerShape(6.dp))
                .background(DarkSurfaceVariant)
        ) {
            Box(
                modifier = Modifier
                    .fillMaxHeight()
                    .fillMaxWidth(fraction = animatedSoc)
                    .clip(RoundedCornerShape(6.dp))
                    .background(gradientBrush)
            )
        }

        Spacer(modifier = Modifier.height(12.dp))

        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween
        ) {
            InfoChip(label = "Voltage", value = "%.1fV".format(voltage))
            InfoChip(label = "Temp", value = "%.1f°C".format(temperature))
            InfoChip(label = "Health", value = healthStatus)
        }
    }
}

@Composable
private fun InfoChip(label: String, value: String) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text(
            text = label,
            fontSize = 11.sp,
            color = TextMuted
        )
        Text(
            text = value,
            fontSize = 13.sp,
            fontWeight = FontWeight.Medium,
            color = TextSecondary
        )
    }
}
