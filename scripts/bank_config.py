# -*- coding: utf-8 -*-
"""Shared counts for ICT question bank rebuild scripts."""

SECTIONS_COUNT = 8
# Original design was 50 MCQs/topic; current target is five times that.
MULTIPLIER = 5
BASE_PER_TOPIC = 50

TOPIC_QUESTION_TARGET = BASE_PER_TOPIC * MULTIPLIER
TOTAL_EXPECTED_MCQS = SECTIONS_COUNT * TOPIC_QUESTION_TARGET
