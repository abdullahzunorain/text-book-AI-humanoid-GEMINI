import React, { useState, type ReactNode } from 'react';
import Layout from '@theme-original/DocItem/Layout';
import type LayoutType from '@theme/DocItem/Layout';
import type { WrapperProps } from '@docusaurus/types';
import ReactMarkdown from 'react-markdown';
import ChapterActions from '@site/src/components/ChapterActions';
import { useAuth } from '@site/src/hooks/useAuth';
import { personalize, translate } from '@site/src/services/contentApi';

type Props = WrapperProps<typeof LayoutType>;

export default function LayoutWrapper(props: Props): ReactNode {
  const [transformedContent, setTransformedContent] = useState<string | null>(null);
  const { isAuthenticated, token } = useAuth();

  const getPageContent = (): string => {
    const article = document.querySelector('article');
    return article ? article.innerText : '';
  };

  const getChapterTitle = (): string => {
    const h1 = document.querySelector('article h1');
    return h1 ? h1.textContent || 'Untitled' : 'Untitled';
  };

  const handlePersonalize = async () => {
    const content = getPageContent();
    if (!content) return;
    try {
      const result = await personalize(content, getChapterTitle(), token);
      setTransformedContent(result);
    } catch (err) {
      console.error(err);
    }
  };

  const handleTranslate = async () => {
    const content = getPageContent();
    if (!content) return;
    try {
      const result = await translate(content, getChapterTitle(), token);
      setTransformedContent(result);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <>
      <ChapterActions
        isAuthenticated={isAuthenticated}
        isTransformed={!!transformedContent}
        onPersonalize={handlePersonalize}
        onTranslate={handleTranslate}
        onRevert={() => setTransformedContent(null)}
      />

      {transformedContent ? (
        <article
          className="markdown"
          style={{
            border: '2px dashed var(--ifm-color-primary)',
            padding: '20px',
            borderRadius: '10px',
          }}
        >
          <div
            style={{
              marginBottom: '15px',
              fontWeight: 'bold',
              color: 'var(--ifm-color-primary)',
            }}
          >
            This content has been transformed by AI. Click "Revert to Original"
            above to restore.
          </div>
          <ReactMarkdown>{transformedContent}</ReactMarkdown>
        </article>
      ) : (
        <Layout {...props} />
      )}
    </>
  );
}
