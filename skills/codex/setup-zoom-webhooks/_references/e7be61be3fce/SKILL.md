---
name: zoom-rtms
description: Use when using RTMS.
---

# Zoom Realtime Media Streams

Use this skill when the integration needs real-time meeting or contact-center media as a backend stream. If the workflow needs a visible participant bot, compare against `build-zoom-bot` and `zoom-meeting-sdk-linux` before choosing RTMS.

## Workflow

1. Confirm the source surface: Meetings RTMS, Contact Center voice media, or another documented RTMS stream.
2. Decide whether RTMS is sufficient or whether a Meeting SDK bot is required for participant identity, meeting controls, or UI-visible behavior.
3. Implement the WebSocket lifecycle first: event subscription, connection validation, media start, heartbeat, reconnect, and shutdown.
4. Process media types intentionally: audio, video, screen share, chat, live transcript, and metadata have different payload and timing constraints.
5. Design downstream pipelines for buffering, transcription, AI analysis, recording, or tool invocation.
6. Debug by isolating app setup, webhook/event delivery, stream authorization, network connectivity, and media payload decoding.

## References

- Full preserved guide: [references/full-guide.md](../7e3a6df60f4d/full-guide.md)
- Connection architecture: [concepts/connection-architecture.md](../82b72cfe10a2/connection-architecture.md)
- Lifecycle flow: [concepts/lifecycle-flow.md](../301ee5a547db/lifecycle-flow.md)
- Media types: [references/media-types.md](../d8a6ecd50e26/media-types.md)
- Data types: [references/data-types.md](../01db64bc6ef9/data-types.md)
- RTMS bot example: [examples/rtms-bot.md](../e0e3847cb99d/rtms-bot.md)
- Common issues: [troubleshooting/common-issues.md](../079e928a0851/common-issues.md)
