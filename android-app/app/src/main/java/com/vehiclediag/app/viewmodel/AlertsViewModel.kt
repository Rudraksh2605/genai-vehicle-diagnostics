package com.vehiclediag.app.viewmodel

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.vehiclediag.app.data.models.AlertModel
import com.vehiclediag.app.network.RetrofitClient
import kotlinx.coroutines.delay
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

/**
 * ViewModel for the Alerts screen.
 * Fetches alert data every 2 seconds using coroutines.
 */
class AlertsViewModel : ViewModel() {

    private val api = RetrofitClient.apiService

    private val _alerts = MutableStateFlow<List<AlertModel>>(emptyList())
    val alerts: StateFlow<List<AlertModel>> = _alerts.asStateFlow()

    private val _isLoading = MutableStateFlow(true)
    val isLoading: StateFlow<Boolean> = _isLoading.asStateFlow()

    private val _error = MutableStateFlow<String?>(null)
    val error: StateFlow<String?> = _error.asStateFlow()

    private val _isPolling = MutableStateFlow(true)

    init {
        startPolling()
    }

    private fun startPolling() {
        viewModelScope.launch {
            while (_isPolling.value) {
                fetchAlerts()
                delay(2000)
            }
        }
    }

    private suspend fun fetchAlerts() {
        try {
            val data = api.getAlerts(limit = 50)
            _alerts.value = data
            _error.value = null
            _isLoading.value = false
        } catch (e: Exception) {
            _error.value = "Connection error: ${e.localizedMessage}"
            _isLoading.value = false
        }
    }

    fun refresh() {
        viewModelScope.launch {
            _isLoading.value = true
            fetchAlerts()
        }
    }

    override fun onCleared() {
        super.onCleared()
        _isPolling.value = false
    }
}
