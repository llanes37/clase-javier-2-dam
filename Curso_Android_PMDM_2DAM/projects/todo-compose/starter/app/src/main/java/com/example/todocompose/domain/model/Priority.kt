package com.example.todocompose.domain.model

enum class Priority {
    HIGH,
    MEDIUM,
    LOW;
    
    companion object {
        fun fromOrdinal(ordinal: Int): Priority {
            return entries.getOrElse(ordinal) { MEDIUM }
        }
    }
}
