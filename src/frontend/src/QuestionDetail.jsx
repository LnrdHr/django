import { useState, useEffect } from 'react';
import axios from 'axios';

export default function QuestionDetail({ questionId, onBack, onVote }) {
  const [question, setQuestion] = useState(null);
  const [selectedChoice, setSelectedChoice] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchQuestionDetail();
  }, [questionId]);

  const fetchQuestionDetail = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`/api/questions/${questionId}/`);
      setQuestion(response.data);
      setError('');
    } catch (error) {
      console.error('Error fetching question detail:', error);
      setError('Failed to load question details');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!selectedChoice) {
      setError('Please select a choice');
      return;
    }

    try {
      const response = await axios.post(`/api/questions/${questionId}/vote/`, {
        choice_id: parseInt(selectedChoice)
      });
      
      // Pass the results to parent component
      onVote(response.data);
    } catch (error) {
      console.error('Error submitting vote:', error);
      setError('Failed to submit vote');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-800 to-slate-600">
        <div className="text-center">
          <span className="loading loading-spinner loading-lg text-white"></span>
          <p className="mt-4 text-white">Loading question...</p>
        </div>
      </div>
    );
  }

  if (!question) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-800 to-slate-600">
        <div className="text-center">
          <p className="text-red-400 text-lg">Failed to load question</p>
          <button onClick={onBack} className="btn btn-primary mt-4">
            Back to Questions
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-800 to-slate-600 p-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="flex items-center justify-between mb-8">
          <button 
            onClick={onBack} 
            className="btn btn-ghost text-white hover:bg-white/10"
          >
            ← Back to Questions
          </button>
        </div>

        {/* Question Card */}
        <div className="card bg-white/95 backdrop-blur-lg shadow-2xl">
          <div className="card-body p-8">
            <h1 className="text-3xl font-bold text-center mb-8 text-gray-800">
              {question.question_text}
            </h1>

            {error && (
              <div className="alert alert-error mb-6">
                <span>{error}</span>
              </div>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
              <div className="space-y-4">
                {question.choices.map((choice, index) => (
                  <div key={choice.id} className="form-control">
                    <label className="label cursor-pointer justify-start gap-4 p-4 rounded-lg hover:bg-gray-50 transition-colors">
                      <input
                        type="radio"
                        name="choice"
                        value={choice.id}
                        className="radio radio-primary"
                        checked={selectedChoice === choice.id.toString()}
                        onChange={(e) => setSelectedChoice(e.target.value)}
                      />
                      <span className="label-text text-lg font-medium text-gray-700">
                        {choice.choice_text}
                      </span>
                    </label>
                  </div>
                ))}
              </div>

              <div className="card-actions justify-center mt-8">
                <button type="submit" className="btn btn-primary btn-lg px-12">
                  Vote
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}
