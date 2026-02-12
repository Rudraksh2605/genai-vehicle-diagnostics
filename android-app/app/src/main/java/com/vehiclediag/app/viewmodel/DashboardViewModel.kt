package com.vehiclediag.app.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.vehiclediag.app.data.models.SimulationStatus
import com.vehiclediag.app.data.models.VehicleTelemetry
import com.vehiclediag.app.network.RetrofitClient
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

/**
 * ViewModel for the Dashboard screen.
 * Fetches vehicle telemetry data every 1 second using coroutines.
 * Implements MVVM pattern with StateFlow for reactive UI updates.
 */
class DashboardViewModel : ViewModel() {

    private val api = RetrofitClient.apiService

    // ── State ───────────────────────────────────────────────────────

    private val _telemetry = MutableStateFlow(VehicleTelemetry())
    val telemetry: StateFlow<VehicleTelemetry> = _telemetry.asStateFlow()

    private val _isLoading = MutableStateFlow(true)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()

    private val _error = MutableStateFlow<String?>(null)
    val error: StateFlow<String?> = _error.asStateFlow()

    private val _simulationStatus = MutableStateFlow(SimulationStatus())
    val simulationStatus: StateFlow<SimulationStatus> = _simulationStatus.asStateFlow()

    private val _isPolling = MutableStateFlow(true)
    val isPolling: StateFlow<Boolean> = _isPolling.asStateFlow()

    // ── Lifecycle ───────────────────────────────────────────────────

    init {
        startPolling()
    }

    /**
     * Start polling telemetry data every 1 second.
     */
    private fun startPolling() {
        viewModelScope.launch {
            while (_isPolling.value) {
                fetchTelemetry()
                delay(1000)
            }
        }
    }

    /**
     * Fetch the latest telemetry snapshot from backend.
     */
    private suspend fun fetchTelemetry() {
        try {
            val data = api.getAllTelemetry()
            _telemetry.value = data
            _error.value = null
            _isLoading.value = false
        } catch (e: Exception) {
            _error.value = "Connection error: ${e.localizedMessage}"
            _isLoading.value = false
        }
    }

    // ── Simulation Control ──────────────────────────────────────────

    fun startSimulation() {
        viewModelScope.launch {
            try {
                val status = api.startSimulation()
                _simulationStatus.value = status
                _error.value = null
            } catch (e: Exception) {
                _error.value = "Failed to start simulation: ${e.localizedMessage}"
            }
        }
    }

    fun stopSimulation() {
        viewModelScope.launch {
            try {
                val status = api.stopSimulation()
                _simulationStatus.value = status
            } catch (e: Exception) {
                _error.value = "Failed to stop simulation: ${e.localizedMessage}"
            }
        }
    }

    fun fetchSimulationStatus() {
        viewModelScope.launch {
            try {
                val status = api.getSimulationStatus()
                _simulationStatus.value = status
            } catch (_: Exception) { }
        }
    }

    fun clearError() {
        _error.value = null
    }

    override fun onCleared() {
        super.onCleared()
        _isPolling.value = false
    }
}
