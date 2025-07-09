# Persian Telegram Bot - Replit Documentation

## Overview

This is a personalized Persian Telegram bot designed specifically for a user named "Behnoosh" with an AI assistant personality named "Amir". The bot provides conversational AI capabilities, music search functionality, Persian jokes, and text-to-speech services, all optimized for Persian language interactions.

## System Architecture

### Core Architecture Pattern
- **Modular Handler-Based Design**: Separates command handling, message processing, and service logic into distinct modules
- **Service-Oriented Architecture**: Each major feature (chat, music, TTS) is encapsulated in dedicated service classes
- **Configuration-Driven Setup**: Centralized configuration management with environment variable support and fallback defaults

### Technology Stack
- **Runtime**: Python 3.x
- **Bot Framework**: python-telegram-bot library
- **TTS Services**: Google Text-to-Speech (gTTS) with ElevenLabs voice cloning support
- **AI Integration**: Google Gemini API for conversational responses
- **Music APIs**: YouTube Data API and RadioJavan integration
- **Deployment**: Designed for cloud deployment with webhook support

## Key Components

### 1. Main Application (`main.py`)
- **Purpose**: Entry point and application orchestration
- **Responsibilities**: Bot initialization, handler registration, logging configuration
- **Architecture Decision**: Uses the Application pattern from python-telegram-bot for clean handler management

### 2. Configuration Management (`config.py`)
- **Purpose**: Centralized configuration with environment variable support
- **Features**: API key management, bot personality settings, file path configuration
- **Architecture Decision**: Single configuration class with validation to ensure all required settings are present

### 3. Handler System
- **Command Handlers** (`handlers/commands.py`): Processes slash commands like /start, /song, /joke
- **Message Handlers** (`handlers/messages.py`): Handles free-form text conversations
- **Architecture Decision**: Separation allows for different processing logic and easier maintenance

### 4. Service Layer
- **Chat Service** (`services/chat_service.py`): AI-powered conversation with fallback response templates
- **Music Service** (`services/music_service.py`): Multi-source music search with Persian music platform integration
- **TTS Service** (`services/tts_service.py`): Text-to-speech with voice cloning capabilities

### 5. Utilities
- **Persian Helpers** (`utils/helpers.py`): Text normalization and Persian language processing
- **Persian Jokes** (`utils/persian_jokes.py`): Curated collection of family-friendly Persian jokes

## Data Flow

### Message Processing Flow
1. **Input Reception**: Telegram updates received via webhook or polling
2. **Handler Routing**: Commands routed to CommandHandlers, text messages to MessageHandlers
3. **Service Processing**: Handlers invoke appropriate services (chat, music, TTS)
4. **Response Generation**: Services return processed content
5. **Multi-modal Output**: Text responses sent with optional voice messages

### API Integration Flow
- **Primary**: Gemini API for intelligent responses
- **Fallback**: Template-based responses for reliability
- **Music Search**: RadioJavan → YouTube API → graceful degradation
- **TTS**: ElevenLabs voice cloning → Google TTS fallback

## External Dependencies

### Required APIs
- **Telegram Bot API**: Core bot functionality (token required)
- **Google Gemini API**: AI-powered conversations (optional)
- **YouTube Data API**: Music search fallback (optional)
- **ElevenLabs API**: Premium voice cloning (optional)

### Python Packages
- `python-telegram-bot`: Telegram bot framework
- `gtts`: Google Text-to-Speech
- `requests`: HTTP client for API calls

### Architecture Decisions
- **Graceful Degradation**: All external APIs have fallback mechanisms
- **Environment-Based Configuration**: Supports development and production environments
- **Optional Feature Detection**: Services adapt based on available API keys

## Deployment Strategy

### Environment Support
- **Development**: Local execution with polling
- **Production**: Webhook-based deployment with cloud hosting
- **Configuration**: Environment variables for sensitive data

### File Management
- **Temporary Audio Storage**: Local directory for TTS file generation
- **Cleanup Strategy**: Temporary files managed per session

### Scaling Considerations
- **Stateless Design**: No persistent storage requirements
- **Rate Limiting**: Built-in message length and audio duration limits
- **Resource Management**: Temporary file cleanup and memory-efficient processing

## Changelog

```
Changelog:
- July 08, 2025. Initial setup
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```