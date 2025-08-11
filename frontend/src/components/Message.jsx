import React from 'react'
import { Bot, User } from 'lucide-react'

const Message = ({ message }) => {
  const isUser = message.type === 'user'
  const timestamp = message.timestamp.toLocaleTimeString([], { 
    hour: '2-digit', 
    minute: '2-digit' 
  })

  return (
    <div className={`flex items-start space-x-3 ${isUser ? 'justify-end' : 'justify-start'}`}>
      {!isUser && (
        <div className="w-8 h-8 bg-primary-500 rounded-full flex items-center justify-center flex-shrink-0">
          <Bot className="h-5 w-5 text-white" />
        </div>
      )}
      
      <div className={`
        max-w-4xl px-4 py-3 rounded-lg shadow-sm
        ${isUser 
          ? 'bg-primary-500 text-white ml-auto' 
          : 'bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 text-gray-900 dark:text-gray-100'
        }
      `}>
        <div className="whitespace-pre-wrap">{message.content}</div>
        <div className={`
          text-xs mt-2 opacity-70
          ${isUser ? 'text-primary-100' : 'text-gray-500 dark:text-gray-400'}
        `}>
          {timestamp}
        </div>
      </div>
      
      {isUser && (
        <div className="w-8 h-8 bg-gray-300 dark:bg-gray-600 rounded-full flex items-center justify-center flex-shrink-0">
          <User className="h-5 w-5 text-gray-600 dark:text-gray-300" />
        </div>
      )}
    </div>
  )
}

export default Message
