// Simple cookie helper to read the csrftoken cookie
export function getCookie(name) {
  const cookieString = document.cookie;
  if (!cookieString) return null;
  const cookies = cookieString.split(';').map(c => c.trim());
  for (const c of cookies) {
    if (c.startsWith(name + '=')) return decodeURIComponent(c.split('=')[1]);
  }
  return null;
}
