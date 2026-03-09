const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export async function personalize(
  content: string,
  chapterTitle: string,
  token: string | null,
): Promise<string> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}/personalize/`, {
    method: 'POST',
    headers,
    body: JSON.stringify({ content, chapter_title: chapterTitle }),
  });

  if (!response.ok) {
    throw new Error(`Personalization failed: ${response.statusText}`);
  }

  const data = await response.json();
  return data.personalized_content;
}

export async function translate(
  content: string,
  chapterTitle: string,
  token: string | null,
): Promise<string> {
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}/translate/`, {
    method: 'POST',
    headers,
    body: JSON.stringify({ content, chapter_title: chapterTitle }),
  });

  if (!response.ok) {
    throw new Error(`Translation failed: ${response.statusText}`);
  }

  const data = await response.json();
  return data.translated_content;
}
