package com.vehiclediag.app.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.CircleShape
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
import com.vehiclediag.app.data.models.AlertModel
import com.vehiclediag.app.ui.theme.*

/**
 * AlertBanner composable — Displays a single alert with severity-colored
 * indicator, message, and timestamp.
 */
@Composable
fun AlertBanner(
    alert: AlertModel,
    modifier: Modifier = Modifier
) {
    val severityColor = when (alert.severity.lowercase()) {
        "critical" -> SeverityCritical
        "warning" -> SeverityWarning
        else -> SeverityInfo
    }

    val severityIcon = when (alert.severity.lowercase()) {
        "critical" -> "🔴"
        "warning" -> "🟠"
        else -> "🔵"
    }

    Row(
        modifier = modifier
            .fillMaxWidth()
            .clip(RoundedCornerShape(12.dp))
            .background(DarkCard)
            .padding(12.dp),
        verticalAlignment = Alignment.Top
    ) {
        // Severity indicator dot
        Box(
            modifier = Modifier
                .padding(top = 4.dp)
                .size(10.dp)
                .clip(CircleShape)
                .background(severityColor)
        )

        Spacer(modifier = Modifier.width(12.dp))

        Column(modifier = Modifier.weight(1f)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text(
                    text = alert.alertType.replace("_", " ").uppercase(),
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    color = severityColor,
                    letterSpacing = 0.5.sp
                )
                Text(
                    text = alert.severity.uppercase(),
                    fontSize = 10.sp,
                    fontWeight = FontWeight.Bold,
                    color = severityColor,
                    modifier = Modifier
                        .clip(RoundedCornerShape(4.dp))
                        .background(severityColor.copy(alpha = 0.15f))
                        .padding(horizontal = 6.dp, vertical = 2.dp)
                )
            }

            Spacer(modifier = Modifier.height(4.dp))

            Text(
                text = alert.message,
                fontSize = 13.sp,
                color = TextPrimary,
                lineHeight = 18.sp
            )

            Spacer(modifier = Modifier.height(6.dp))

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(
                    text = "Signal: ${alert.signal}",
                    fontSize = 10.sp,
                    color = TextMuted
                )
                Text(
                    text = formatTimestamp(alert.timestamp),
                    fontSize = 10.sp,
                    color = TextMuted
                )
            }
        }
    }
}

/**
 * Format ISO timestamp for display.
 */
private fun formatTimestamp(timestamp: String): String {
    return try {
        // Extract time portion from ISO timestamp
        val timePart = timestamp.substringAfter("T").take(8)
        timePart
    } catch (e: Exception) {
        timestamp.takeLast(8)
    }
}
