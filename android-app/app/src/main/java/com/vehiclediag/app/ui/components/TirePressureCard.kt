package com.vehiclediag.app.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.vehiclediag.app.ui.theme.*

/**
 * TirePressureCard composable — Shows tire pressure for one tire with
 * color-coded status indicator.
 */
@Composable
fun TirePressureCard(
    label: String,
    pressure: Double,
    modifier: Modifier = Modifier
) {
    val statusColor = when {
        pressure < 25.0 -> GaugeRed
        pressure < 28.0 -> GaugeYellow
        else -> GaugeGreen
    }

    val statusText = when {
        pressure < 25.0 -> "CRITICAL"
        pressure < 28.0 -> "LOW"
        else -> "OK"
    }

    Column(
        horizontalAlignment = Alignment.CenterHorizontally,
        modifier = modifier
            .clip(RoundedCornerShape(12.dp))
            .background(DarkCard)
            .padding(12.dp)
            .widthIn(min = 80.dp)
    ) {
        Text(
            text = label,
            fontSize = 11.sp,
            color = TextMuted,
            fontWeight = FontWeight.Medium
        )

        Spacer(modifier = Modifier.height(6.dp))

        Text(
            text = "%.1f".format(pressure),
            fontSize = 22.sp,
            fontWeight = FontWeight.Bold,
            color = TextPrimary
        )

        Text(
            text = "PSI",
            fontSize = 10.sp,
            color = TextSecondary
        )

        Spacer(modifier = Modifier.height(6.dp))

        Box(
            modifier = Modifier
                .clip(RoundedCornerShape(4.dp))
                .background(statusColor.copy(alpha = 0.2f))
                .padding(horizontal = 8.dp, vertical = 2.dp)
        ) {
            Text(
                text = statusText,
                fontSize = 9.sp,
                fontWeight = FontWeight.Bold,
                color = statusColor
            )
        }
    }
}

/**
 * TirePressureGrid — Shows all 4 tires in a 2x2 grid matching tire positions.
 */
@Composable
fun TirePressureGrid(
    frontLeft: Double,
    frontRight: Double,
    rearLeft: Double,
    rearRight: Double,
    modifier: Modifier = Modifier
) {
    Column(
        modifier = modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(16.dp))
            .background(DarkCard)
            .padding(16.dp)
    ) {
        Text(
            text = "🛞 Tire Pressure",
            style = MaterialTheme.typography.titleMedium,
            fontWeight = FontWeight.SemiBold,
            color = TextPrimary
        )

        Spacer(modifier = Modifier.height(12.dp))

        // Front tires
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceEvenly
        ) {
            TirePressureCard(label = "Front L", pressure = frontLeft)
            TirePressureCard(label = "Front R", pressure = frontRight)
        }

        Spacer(modifier = Modifier.height(8.dp))

        // Rear tires
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceEvenly
        ) {
            TirePressureCard(label = "Rear L", pressure = rearLeft)
            TirePressureCard(label = "Rear R", pressure = rearRight)
        }
    }
}
