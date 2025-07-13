import React from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { useToast } from '@/components/ui/use-toast';
import { Clock, CheckCircle, Github, Star } from 'lucide-react';
import type { Project } from '@/types';

interface ProjectCardProps {
  project: Project;
  onComplete: () => void;
}

export function ProjectCard({ project, onComplete }: ProjectCardProps) {
  const { toast } = useToast();
  
  const getDifficultyColor = (difficulty: string) => {
    switch (difficulty) {
      case 'beginner': return 'bg-green-500';
      case 'intermediate': return 'bg-yellow-500';
      case 'advanced': return 'bg-red-500';
      default: return 'bg-gray-500';
    }
  };

  const handleGitHubClick = () => {
    if (project.github_url) {
      window.open(project.github_url, '_blank');
    } else {
      toast({
        title: "🚧 No GitHub URL provided."
      });
    }
  };

  const handleLiveClick = () => {
    if (project.live_url) {
      window.open(project.live_url, '_blank');
    } else {
      toast({
        title: "🚧 No live URL provided."
      });
    }
  };

  return (
    <Card className="bg-white/10 backdrop-blur-lg border-white/20 hover:bg-white/15 transition-all duration-200 group">
      <CardHeader>
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <CardTitle className="text-white text-lg mb-2">{project.name}</CardTitle>
            <CardDescription className="text-purple-200">{project.description}</CardDescription>
          </div>
          <Badge className={`${getDifficultyColor(project.difficulty)} text-white ml-2`}>
            {project.difficulty}
          </Badge>
        </div>
      </CardHeader>
      
      <CardContent>
        <div className="space-y-4">
          <div className="flex flex-wrap gap-2">
            {project.technology && (
              <Badge variant="outline" className="border-purple-400 text-purple-300">
                {project.technology}
              </Badge>
            )}
            {project.category && (
              <Badge variant="outline" className="border-blue-400 text-blue-300">
                {project.category}
              </Badge>
            )}
          </div>

          <div className="flex items-center justify-between">
            <div className="flex space-x-2">
              <Button
                size="sm"
                variant="outline"
                onClick={handleGitHubClick}
                className="border-white/20 text-white hover:bg-white/10"
              >
                <Github className="h-4 w-4" />
              </Button>
              <Button
                size="sm"
                variant="outline"
                onClick={handleLiveClick}
                className="border-white/20 text-white hover:bg-white/10"
              >
                <Star className="h-4 w-4" />
              </Button>
            </div>

            {project.status === 'completed' ? (
              <Badge className="bg-green-500 text-white">
                <CheckCircle className="h-3 w-3 mr-1" />
                Completed
              </Badge>
            ) : (
              <Button
                size="sm"
                onClick={onComplete}
                className="bg-gradient-to-r from-green-500 to-emerald-500 hover:from-green-600 hover:to-emerald-600"
              >
                <CheckCircle className="h-4 w-4 mr-1" />
                Complete
              </Button>
            )}
          </div>

          <div className="text-xs text-purple-300">
            <Clock className="h-3 w-3 inline mr-1" />
            Created {new Date(project.created_at).toLocaleDateString()}
          </div>
        </div>
      </CardContent>
    </Card>
  );
}