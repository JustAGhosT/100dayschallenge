import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Header } from '@/components/Header';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { ProjectCard } from '@/components/ProjectCard';
import { ProjectForm } from '@/components/ProjectForm';
import { PortfolioView } from '@/components/PortfolioView';
import { AnalyticsView } from '@/components/AnalyticsView';
import { Calendar, Code, Plus, CheckCircle, TrendingUp, Award } from 'lucide-react';
import { useChallenge } from '@/hooks/useChallenge';
import { useAuth } from '@/contexts/SupabaseAuthContext';

export function Dashboard({ projects, challenge, onAddProject, onCompleteProject, signOut }) {
  const [isAddProjectOpen, setIsAddProjectOpen] = useState(false);
  const { user } = useAuth();
  const { userProfile } = useChallenge(user?.id);

  const getDaysElapsed = () => {
    if (!challenge?.startDate) return 0;
    const now = new Date();
    const diffTime = Math.abs(now - new Date(challenge.startDate));
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  };

  const getCompletedProjects = () => projects.filter(p => p.status === 'completed').length;
  const getProgressPercentage = () => (getCompletedProjects() / (challenge?.goal_apps || 100)) * 100;
  const getDailyAverage = () => {
    const days = getDaysElapsed();
    return days > 0 ? (getCompletedProjects() / days).toFixed(1) : 0;
  };

  return (
    <>
      <Header 
        userProfile={userProfile}
        completedProjects={getCompletedProjects()}
        daysElapsed={getDaysElapsed()}
        signOut={signOut}
      />
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <Card className="bg-gradient-to-br from-purple-500/20 to-purple-600/20 border-purple-400/30 backdrop-blur-lg">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-purple-200 text-sm font-medium">Apps Completed</p>
                    <p className="text-3xl font-bold text-white">{getCompletedProjects()}</p>
                    <p className="text-purple-300 text-xs">out of {challenge.goal_apps}</p>
                  </div>
                  <CheckCircle className="h-8 w-8 text-purple-400" />
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-blue-500/20 to-blue-600/20 border-blue-400/30 backdrop-blur-lg">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-blue-200 text-sm font-medium">Days Elapsed</p>
                    <p className="text-3xl font-bold text-white">{getDaysElapsed()}</p>
                    <p className="text-blue-300 text-xs">since start</p>
                  </div>
                  <Calendar className="h-8 w-8 text-blue-400" />
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-indigo-500/20 to-indigo-600/20 border-indigo-400/30 backdrop-blur-lg">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-indigo-200 text-sm font-medium">Daily Average</p>
                    <p className="text-3xl font-bold text-white">{getDailyAverage()}</p>
                    <p className="text-indigo-300 text-xs">apps per day</p>
                  </div>
                  <TrendingUp className="h-8 w-8 text-indigo-400" />
                </div>
              </CardContent>
            </Card>

            <Card className="bg-gradient-to-br from-green-500/20 to-green-600/20 border-green-400/30 backdrop-blur-lg">
              <CardContent className="p-6">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-green-200 text-sm font-medium">Progress</p>
                    <p className="text-3xl font-bold text-white">{getProgressPercentage().toFixed(1)}%</p>
                    <p className="text-green-300 text-xs">completed</p>
                  </div>
                  <Award className="h-8 w-8 text-green-400" />
                </div>
              </CardContent>
            </Card>
          </div>

          <Card className="mb-8 bg-white/10 backdrop-blur-lg border-white/20">
            <CardContent className="p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-white">{challenge.name} Progress</h3>
                <span className="text-purple-300 font-medium">{getCompletedProjects()}/{challenge.goal_apps} Apps</span>
              </div>
              <Progress value={getProgressPercentage()} className="h-3 bg-white/10" />
            </CardContent>
          </Card>

          <Tabs defaultValue="projects" className="space-y-6">
            <TabsList className="bg-white/10 backdrop-blur-lg border border-white/20 p-1">
              <TabsTrigger value="projects" className="data-[state=active]:bg-purple-500 data-[state=active]:text-white">
                Projects
              </TabsTrigger>
              <TabsTrigger value="portfolio" className="data-[state=active]:bg-purple-500 data-[state=active]:text-white">
                Portfolio
              </TabsTrigger>
              <TabsTrigger value="analytics" className="data-[state=active]:bg-purple-500 data-[state=active]:text-white">
                Analytics
              </TabsTrigger>
            </TabsList>

            <TabsContent value="projects">
              <div className="flex justify-between items-center mb-6">
                <h2 className="text-2xl font-bold text-white">Your Projects</h2>
                <Dialog open={isAddProjectOpen} onOpenChange={setIsAddProjectOpen}>
                  <DialogTrigger asChild>
                    <Button className="bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600">
                      <Plus className="h-4 w-4 mr-2" />
                      Add Project
                    </Button>
                  </DialogTrigger>
                  <DialogContent className="bg-gray-900 border-gray-700">
                    <DialogHeader>
                      <DialogTitle className="text-white">Add New Project</DialogTitle>
                    </DialogHeader>
                    <ProjectForm 
                      onSubmit={(data) => {
                        onAddProject(data);
                        setIsAddProjectOpen(false);
                      }} 
                    />
                  </DialogContent>
                </Dialog>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <AnimatePresence>
                  {projects.map((project, index) => (
                    <motion.div
                      key={project.id}
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      exit={{ opacity: 0, y: -20 }}
                      transition={{ delay: index * 0.1 }}
                    >
                      <ProjectCard 
                        project={project} 
                        onComplete={() => onCompleteProject(project.id)}
                      />
                    </motion.div>
                  ))}
                </AnimatePresence>
              </div>

              {projects.length === 0 && (
                <div className="text-center py-12">
                  <Code className="h-16 w-16 text-purple-400 mx-auto mb-4 opacity-50" />
                  <p className="text-purple-200 text-lg">No projects yet. Add your first project to get started!</p>
                </div>
              )}
            </TabsContent>

            <TabsContent value="portfolio">
              <PortfolioView projects={projects} userProfile={userProfile} />
            </TabsContent>

            <TabsContent value="analytics">
              <AnalyticsView projects={projects} challenge={challenge} />
            </TabsContent>
          </Tabs>
        </motion.div>
      </div>
    </>
  );
}