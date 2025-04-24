export function getQuery(window)
{
	const URL = new URLSearchParams(window.location.search)
	return URL.get('user_id')
}