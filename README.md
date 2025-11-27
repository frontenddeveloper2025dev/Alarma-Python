Alarm Tool Project
Overview

This is a Spanish-language alarm management application built with Streamlit that allows users to create, manage, and monitor recurring weekly alarms. The system features a web-based interface for alarm configuration and a background monitoring service that plays audio notifications when alarms trigger. The application supports setting alarms for specific times and days of the week, with automatic audio playback using generated alarm sounds.
User Preferences

Preferred communication style: Simple, everyday language.
System Architecture
Frontend Architecture

    Web Framework: Streamlit-based web application providing a simple, interactive interface
    User Interface: Single-page application with sidebar for alarm creation and main area for alarm management
    State Management: Uses Streamlit's session state to maintain application state across user interactions
    Language: Spanish interface for user-facing elements

Backend Architecture

    Core Components:
        AlarmMonitor: Background service that continuously checks for alarms to trigger
        AlarmDatabase: SQLite-based data persistence layer for alarm storage and history
        AudioPlayer: Audio playback system using pygame for alarm notifications
        AlarmSoundGenerator: Programmatic alarm sound generation using numpy

    Threading Model:
        Main Streamlit application runs on primary thread
        Background alarm monitoring runs on separate daemon thread
        Audio playback executes on dedicated threads to prevent UI blocking

    Monitoring Logic:
        Checks for active alarms every 30 seconds
        Prevents duplicate alarm triggers within the same day
        Automatic reset of triggered alarms at midnight

Data Storage

    Database: SQLite with two main tables:
        alarms: Stores alarm configurations (name, time, days, active status)
        alarm_history: Tracks alarm trigger events for auditing
    Data Format: JSON serialization for day-of-week arrays, time stored as HH:MM strings
    File Storage: Local SQLite database file (alarms.db)

Audio System

    Sound Generation:
        Numpy-based procedural audio generation
        Creates beeping patterns with multiple frequencies (800Hz and 1000Hz)
        Generates temporary WAV files for playback
    Audio Playback:
        Pygame mixer for cross-platform audio support
        Configurable alarm duration (default 30 seconds)
        Concurrent playback prevention

Error Handling

    Graceful degradation for audio initialization failures
    Exception handling in alarm monitoring loop with extended retry intervals
    Temporary file cleanup for generated audio files

External Dependencies
Python Libraries

    streamlit: Web application framework for the user interface
    pandas: Data manipulation for alarm display and management
    pygame: Audio playback system for alarm notifications
    numpy: Mathematical operations for audio waveform generation
    sqlite3: Built-in Python library for database operations

System Dependencies

    Audio System: Requires system audio capabilities for pygame mixer
    File System: Temporary file creation for audio generation
    Threading: Python threading support for background monitoring

Runtime Requirements

    Python environment with package management
    Audio output device for alarm notifications
    File system write permissions for database and temporary audio files
