import React from 'react';
import { useToast } from '@/components/ui/use-toast';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Progress } from '@/components/ui/progress';
import { Trophy } from 'lucide-react';

export function AnalyticsView({ projects, challenge }) {
  const { toast } = useToast();
  
  const completedProjects = projects.filter(p => p.status === 'completed');
  const technologies = [...new Set(projects.map(p => p.technology).filter(Boolean))];
  const categories = [...new Set(projects.map(p => p.category).filter(Boolean))];

  const showDetailedAnalytics = () => {
    toast({
      title: "🚧 This feature isn't implemented yet—but don't worry! You can request it in your next prompt! 🚀"
    });
  };

  const milestones = [
    Math.floor(challenge.goal_apps * 0.25),
    Math.floor(challenge.goal_apps * 0.5),
    Math.floor(challenge.goal_apps * 0.75),
    challenge.goal_apps
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-white">Analytics & Insights</h2>
        <Button onClick={showDetailedAnalytics} className="bg-gradient-to-r from-purple-500 to-blue-500">
          Detailed Analytics
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="bg-white/10 backdrop-blur-lg border-white/20">
          <CardHeader>
            <CardTitle className="text-white">Technologies Used</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {technologies.map((tech) => {
                const count = projects.filter(p => p.technology === tech).length;
                const percentage = projects.length > 0 ? (count / projects.length) * 100 : 0;
                return (
                  <div key={tech} className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-white">{tech}</span>
                      <span className="text-purple-300">{count} projects</span>
                    </div>
                    <Progress value={percentage} className="h-2 bg-white/10" />
                  </div>
                );
              })}
            </div>
            {technologies.length === 0 && (
              <p className="text-purple-200 text-center py-4">No technologies tracked yet</p>
            )}
          </CardContent>
        </Card>

        <Card className="bg-white/10 backdrop-blur-lg border-white/20">
          <CardHeader>
            <CardTitle className="text-white">Project Categories</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {categories.map((category) => {
                const count = projects.filter(p => p.category === category).length;
                const percentage = projects.length > 0 ? (count / projects.length) * 100 : 0;
                return (
                  <div key={category} className="space-y-2">
                    <div className="flex justify-between text-sm">
                      <span className="text-white">{category}</span>
                      <span className="text-purple-300">{count} projects</span>
                    </div>
                    <Progress value={percentage} className="h-2 bg-white/10" />
                  </div>
                );
              })}
            </div>
            {categories.length === 0 && (
              <p className="text-purple-200 text-center py-4">No categories tracked yet</p>
            )}
          </CardContent>
        </Card>
      </div>

      <Card className="bg-white/10 backdrop-blur-lg border-white/20">
        <CardHeader>
          <CardTitle className="text-white">Challenge Milestones</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {milestones.map((milestone) => {
              const isReached = completedProjects.length >= milestone;
              return (
                <div key={milestone} className={`p-4 rounded-lg border ${isReached ? 'bg-green-500/20 border-green-400' : 'bg-white/5 border-white/10'}`}>
                  <div className="text-center">
                    <div className={`w-12 h-12 rounded-full mx-auto mb-2 flex items-center justify-center ${isReached ? 'bg-green-500' : 'bg-gray-600'}`}>
                      <Trophy className="h-6 w-6 text-white" />
                    </div>
                    <p className="text-white font-semibold">{milestone} Apps</p>
                    <p className={`text-sm ${isReached ? 'text-green-300' : 'text-gray-400'}`}>
                      {isReached ? 'Completed!' : 'In Progress'}
                    </p>
                  </div>
                </div>
              );
            })}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}