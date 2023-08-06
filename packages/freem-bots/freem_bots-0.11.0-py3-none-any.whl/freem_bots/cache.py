from typing import Optional
import aiomcache
import aiomcache.client
import base64


class Cache:
	def __init__(self, host: str, port: int) -> None:
		self._client = aiomcache.Client(host, port)

	async def set(self, key: str, data: bytes) -> None:
		await self._client.set(self._get_key(key), data)  # pylint: disable=no-value-for-parameter

	async def get(self, key: str) -> Optional[bytes]:
		try:
			return await self._client.get(self._get_key(key))  # type: ignore
		except aiomcache.ClientException:
			return None

	def _get_key(self, key: str) -> bytes:
		base64_encoded = base64.b64encode(key.encode('utf-8'))
		return base64_encoded
