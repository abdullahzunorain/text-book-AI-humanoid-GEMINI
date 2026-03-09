import React, { useState } from 'react';
import styles from './AuthModal.module.css';

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSignUp: (data: SignUpData) => Promise<void>;
  onSignIn: (email: string, password: string) => Promise<void>;
}

interface SignUpData {
  name: string;
  email: string;
  password: string;
  hardware_background: string;
  software_background: string;
  learning_goal?: string;
}

const HARDWARE_OPTIONS = [
  'No GPU',
  'Integrated GPU',
  'NVIDIA GTX Series',
  'NVIDIA RTX Series',
  'AMD GPU',
  'Apple Silicon',
  'Cloud GPU (Colab/AWS)',
];

const SOFTWARE_OPTIONS = [
  'Beginner (no programming)',
  'Basic Python',
  'Intermediate Python',
  'Advanced Python',
  'ROS/ROS 2 experience',
  'ML/AI experience',
];

const AuthModal: React.FC<AuthModalProps> = ({ isOpen, onClose, onSignUp, onSignIn }) => {
  const [tab, setTab] = useState<'signin' | 'signup'>('signin');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Sign In state
  const [signInEmail, setSignInEmail] = useState('');
  const [signInPassword, setSignInPassword] = useState('');

  // Sign Up state
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [hardwareBg, setHardwareBg] = useState('');
  const [softwareBg, setSoftwareBg] = useState('');
  const [learningGoal, setLearningGoal] = useState('');

  if (!isOpen) return null;

  const handleSignIn = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);
    try {
      await onSignIn(signInEmail, signInPassword);
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Sign in failed');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSignUp = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);
    try {
      await onSignUp({
        name,
        email,
        password,
        hardware_background: hardwareBg,
        software_background: softwareBg,
        learning_goal: learningGoal || undefined,
      });
      onClose();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Sign up failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={styles.overlay} onClick={onClose}>
      <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
        <button className={styles.closeBtn} onClick={onClose}>x</button>

        <div className={styles.tabs}>
          <button
            className={`${styles.tab} ${tab === 'signin' ? styles.activeTab : ''}`}
            onClick={() => { setTab('signin'); setError(null); }}
          >
            Sign In
          </button>
          <button
            className={`${styles.tab} ${tab === 'signup' ? styles.activeTab : ''}`}
            onClick={() => { setTab('signup'); setError(null); }}
          >
            Sign Up
          </button>
        </div>

        {error && <div className={styles.error}>{error}</div>}

        {tab === 'signin' ? (
          <form onSubmit={handleSignIn} className={styles.form}>
            <label className={styles.label}>
              Email
              <input
                type="email"
                value={signInEmail}
                onChange={(e) => setSignInEmail(e.target.value)}
                required
                className={styles.input}
              />
            </label>
            <label className={styles.label}>
              Password
              <input
                type="password"
                value={signInPassword}
                onChange={(e) => setSignInPassword(e.target.value)}
                required
                className={styles.input}
              />
            </label>
            <button type="submit" className={styles.submitBtn} disabled={isLoading}>
              {isLoading ? 'Signing in...' : 'Sign In'}
            </button>
          </form>
        ) : (
          <form onSubmit={handleSignUp} className={styles.form}>
            <label className={styles.label}>
              Name
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                className={styles.input}
              />
            </label>
            <label className={styles.label}>
              Email
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                className={styles.input}
              />
            </label>
            <label className={styles.label}>
              Password
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                minLength={6}
                className={styles.input}
              />
            </label>
            <label className={styles.label}>
              Hardware Background
              <select
                value={hardwareBg}
                onChange={(e) => setHardwareBg(e.target.value)}
                required
                className={styles.input}
              >
                <option value="">Select...</option>
                {HARDWARE_OPTIONS.map(opt => (
                  <option key={opt} value={opt}>{opt}</option>
                ))}
              </select>
            </label>
            <label className={styles.label}>
              Software Background
              <select
                value={softwareBg}
                onChange={(e) => setSoftwareBg(e.target.value)}
                required
                className={styles.input}
              >
                <option value="">Select...</option>
                {SOFTWARE_OPTIONS.map(opt => (
                  <option key={opt} value={opt}>{opt}</option>
                ))}
              </select>
            </label>
            <label className={styles.label}>
              Learning Goal (optional)
              <input
                type="text"
                value={learningGoal}
                onChange={(e) => setLearningGoal(e.target.value)}
                placeholder="e.g., Career transition to robotics"
                className={styles.input}
              />
            </label>
            <button type="submit" className={styles.submitBtn} disabled={isLoading}>
              {isLoading ? 'Creating account...' : 'Sign Up'}
            </button>
          </form>
        )}
      </div>
    </div>
  );
};

export default AuthModal;
