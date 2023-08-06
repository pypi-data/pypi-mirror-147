#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2015-2022 Evgeniy Privalov, https://linkedin.com/in/evgeniyprivalov/

from typing import Optional

from tgsdk import TelegramEntity


class SentWebAppMessage(TelegramEntity):
	__slots__ = (
		"inline_message_id",
	)

	def __init__(
		self,
		inline_message_id: Optional[str] = None
	):
		self.inline_message_id = inline_message_id
