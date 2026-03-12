import React, { useState } from 'react';
import styles from './ChapterActions.module.css';

interface ChapterActionsProps {
  isAuthenticated: boolean;
  isTransformed: boolean;
  onPersonalize: () => Promise<void>;
  onTranslate: () => Promise<void>;
  onRevert: () => void;
}

const ChapterActions: React.FC<ChapterActionsProps> = ({
  isAuthenticated,
  isTransformed,
  onPersonalize,
  onTranslate,
  onRevert,
}) => {
  const [personalizeLoading, setPersonalizeLoading] = useState(false);
  const [translateLoading, setTranslateLoading] = useState(false);

  if (!isAuthenticated) return null;

  const handlePersonalize = async () => {
    setPersonalizeLoading(true);
    try {
      await onPersonalize();
    } finally {
      setPersonalizeLoading(false);
    }
  };

  const handleTranslate = async () => {
    setTranslateLoading(true);
    try {
      await onTranslate();
    } finally {
      setTranslateLoading(false);
    }
  };

  const isLoading = personalizeLoading || translateLoading;

  return (
    <div className={styles.actionBar}>
      <span className={styles.label}>AI Actions:</span>
      <button
        className={`button button--primary button--sm ${styles.actionBtn}`}
        onClick={handlePersonalize}
        disabled={isLoading}
      >
        {personalizeLoading ? 'Personalizing...' : 'Personalize'}
      </button>
      <button
        className={`button button--secondary button--sm ${styles.actionBtn}`}
        onClick={handleTranslate}
        disabled={isLoading}
      >
        {translateLoading ? 'Translating...' : 'Translate to Urdu'}
      </button>
      {isTransformed && (
        <button
          className={`button button--outline button--danger button--sm ${styles.actionBtn}`}
          onClick={onRevert}
        >
          Revert to Original
        </button>
      )}
    </div>
  );
};

export default ChapterActions;
