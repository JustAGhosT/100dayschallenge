import React from 'react';
import { Helmet } from 'react-helmet';
import { useAuth } from '@/contexts/SupabaseAuthContext';
import { useChallenge } from '@/hooks/useChallenge';
import { LandingPage } from '@/components/LandingPage';
import { ChallengeSelection } from '@/components/ChallengeSelection';
import { Dashboard } from '@/components/Dashboard';

function App() {
  const { user, loading, signInWithGitHub, signInWithGoogle, signOut } = useAuth();
  const {
    projects,
    activeChallenge,
    userProfile,
    isLoading: isChallengeLoading,
    startChallenge,
    addProject,
    completeProject,
  } = useChallenge(user?.id);

  const mainContent = () => {
    if (loading || isChallengeLoading) {
      return (
        <div className="flex items-center justify-center h-full">
          <div className="text-white text-2xl">Loading...</div>
        </div>
      );
    }

    if (!user) {
      return (
        <LandingPage
          onSignInGitHub={signInWithGitHub}
          onSignInGoogle={signInWithGoogle}
        />
      );
    }
    
    if (!activeChallenge) {
      return <ChallengeSelection onChallengeSelect={startChallenge} />;
    }

    return (
      <Dashboard
        projects={projects}
        challenge={activeChallenge}
        userProfile={userProfile}
        onAddProject={addProject}
        onCompleteProject={completeProject}
        signOut={signOut}
      />
    );
  };

  return (
    <>
      <Helmet>
        <title>100 Apps in 100 Days Challenge - Track Your Coding Journey</title>
        <meta
          name="description"
          content="Join the ultimate coding challenge! Track, document, and showcase your journey of building 100 applications in 100 days."
        />
      </Helmet>
      <main className="min-h-screen bg-gradient-to-br from-purple-900 via-blue-900 to-indigo-900 text-white">
         <div className="fixed inset-0 overflow-hidden pointer-events-none">
          <div className="absolute -top-40 -right-40 w-80 h-80 bg-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
          <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-blue-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse delay-1000"></div>
          <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-indigo-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse delay-500"></div>
        </div>
        <div className="relative z-10 min-h-screen flex flex-col">
          {mainContent()}
        </div>
      </main>
    </>
  );
}

export default App;