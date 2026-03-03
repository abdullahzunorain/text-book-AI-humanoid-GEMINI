import React, { useState, useEffect, type ReactNode } from 'react';
import Layout from '@theme-original/DocItem/Layout';
import type LayoutType from '@theme/DocItem/Layout';
import type {WrapperProps} from '@docusaurus/types';
import ReactMarkdown from 'react-markdown';

type Props = WrapperProps<typeof LayoutType>;

export default function LayoutWrapper(props: Props): ReactNode {
  const [transformedContent, setTransformedContent] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [userId, setUserId] = useState<number>(1); // Mock user ID

  const handleAction = async (action: 'personalize' | 'translate') => {
    // Attempt to grab text from the article element, or body
    const article = document.querySelector('article');
    if (!article) return;
    const content = article.innerText;

    setLoading(true);
    try {
      const url = `http://localhost:8000/${action}/`;
      const payload = action === 'personalize' 
        ? { user_id: userId, content } 
        : { content };

      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.statusText}`);
      }

      const data = await response.json();
      setTransformedContent(data.content);
    } catch (err) {
      console.error(err);
      alert(`Failed to ${action} content.`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div style={{ marginBottom: '1rem', display: 'flex', gap: '1rem', justifyContent: 'flex-end', background: 'var(--ifm-color-emphasis-100)', padding: '10px', borderRadius: '8px' }}>
        <span style={{ margin: 'auto 0 auto 0', fontWeight: 'bold' }}>Interactive Book Features:</span>
        <button 
          className="button button--primary button--sm" 
          onClick={() => handleAction('personalize')}
          disabled={loading}
        >
          {loading ? 'Processing...' : 'Personalize Content'}
        </button>
        <button 
          className="button button--secondary button--sm" 
          onClick={() => handleAction('translate')}
          disabled={loading}
        >
          {loading ? 'Processing...' : 'Translate to Urdu'}
        </button>
        {transformedContent && (
          <button 
            className="button button--outline button--danger button--sm" 
            onClick={() => setTransformedContent(null)}
          >
            Reset
          </button>
        )}
      </div>

      {transformedContent ? (
        <article className="markdown" style={{ border: '2px dashed var(--ifm-color-primary)', padding: '20px', borderRadius: '10px' }}>
          <div style={{ marginBottom: '15px', fontWeight: 'bold', color: 'var(--ifm-color-primary)' }}>
            ⚠️ This content has been transformed by AI.
          </div>
          <ReactMarkdown>{transformedContent}</ReactMarkdown>
        </article>
      ) : (
        <Layout {...props} />
      )}
    </>
  );
}
