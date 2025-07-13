
import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';

export function ProjectForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    technology: '',
    category: '',
    github_url: '',
    live_url: '',
    difficulty: 'beginner'
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
    setFormData({
      name: '',
      description: '',
      technology: '',
      category: '',
      github_url: '',
      live_url: '',
      difficulty: 'beginner'
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <Label htmlFor="name" className="text-white">Project Name</Label>
        <Input
          id="name"
          value={formData.name}
          onChange={(e) => setFormData({...formData, name: e.target.value})}
          className="bg-gray-800 border-gray-600 text-white"
          required
        />
      </div>
      
      <div>
        <Label htmlFor="description" className="text-white">Description</Label>
        <Textarea
          id="description"
          value={formData.description}
          onChange={(e) => setFormData({...formData, description: e.target.value})}
          className="bg-gray-800 border-gray-600 text-white"
          rows={3}
        />
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <Label htmlFor="technology" className="text-white">Technology</Label>
          <Input
            id="technology"
            value={formData.technology}
            onChange={(e) => setFormData({...formData, technology: e.target.value})}
            className="bg-gray-800 border-gray-600 text-white"
            placeholder="React, Vue, etc."
          />
        </div>
        
        <div>
          <Label htmlFor="category" className="text-white">Category</Label>
          <Input
            id="category"
            value={formData.category}
            onChange={(e) => setFormData({...formData, category: e.target.value})}
            className="bg-gray-800 border-gray-600 text-white"
            placeholder="Web App, Game, etc."
          />
        </div>
      </div>

      <div>
        <Label htmlFor="difficulty" className="text-white">Difficulty</Label>
        <Select value={formData.difficulty} onValueChange={(value) => setFormData({...formData, difficulty: value})}>
          <SelectTrigger className="bg-gray-800 border-gray-600 text-white">
            <SelectValue />
          </SelectTrigger>
          <SelectContent className="bg-gray-800 border-gray-600">
            <SelectItem value="beginner">Beginner</SelectItem>
            <SelectItem value="intermediate">Intermediate</SelectItem>
            <SelectItem value="advanced">Advanced</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <Label htmlFor="github_url" className="text-white">GitHub URL</Label>
          <Input
            id="github_url"
            value={formData.github_url}
            onChange={(e) => setFormData({...formData, github_url: e.target.value})}
            className="bg-gray-800 border-gray-600 text-white"
            placeholder="https://github.com/..."
          />
        </div>
        
        <div>
          <Label htmlFor="live_url" className="text-white">Live URL</Label>
          <Input
            id="live_url"
            value={formData.live_url}
            onChange={(e) => setFormData({...formData, live_url: e.target.value})}
            className="bg-gray-800 border-gray-600 text-white"
            placeholder="https://..."
          />
        </div>
      </div>

      <Button type="submit" className="w-full bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600">
        Add Project
      </Button>
    </form>
  );
}
