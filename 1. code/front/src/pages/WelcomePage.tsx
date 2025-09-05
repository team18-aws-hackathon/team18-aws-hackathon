import { useState } from 'react'
import { MobileContainer, Header, Button, Input } from '@/components'
import { Radio, RadioGroup, FormControlLabel, FormControl, Tooltip } from '@mui/material'
import { HelpOutline } from '@mui/icons-material'

interface WelcomePageProps {
  onComplete: () => void
}

export const WelcomePage = ({ onComplete }: WelcomePageProps) => {
  const [name, setName] = useState('')
  const [selectedQuokka, setSelectedQuokka] = useState<'F' | 'T'>('F')

  return (
    <MobileContainer>
      <Header title="Quokka Diary" />
      
      <div className="flex-1 p-6 flex flex-col bg-white">
        {/* Quokka Character */}
        <div className="text-center mb-8">
          <div className="text-8xl mb-4">🐨</div>
          <h2 className="text-2xl mb-2 text-gray-800 font-bold">Welcome!</h2>
          <p className="text-gray-600 text-base">I'm here to listen. What's on your mind?</p>
        </div>

        {/* Name Input */}
        <div className="mb-8">
          <label className="block mb-2 text-gray-800 text-base font-medium">
            Name
          </label>
          <Input 
            placeholder="Enter your name"
            value={name}
            onChange={setName}
          />
        </div>

        {/* Quokka Selection */}
        <div className="mb-8">
          <FormControl component="fieldset" sx={{ width: '100%' }}>
            <label
              className="block mb-2 text-gray-800 text-base font-medium"
            >
              <div className="flex items-center gap-1">
                Choose your Quokka companion
                <Tooltip 
                  title="F Quokka is more feeling-oriented and empathetic. T Quokka is more thinking-oriented and logical. Choose the companion that matches your personality!"
                  arrow
                  placement="top"
                >
                  <HelpOutline className="text-gray-500" sx={{ fontSize: 20 }} />
                </Tooltip>
              </div>
            </label>
            <RadioGroup
              value={selectedQuokka}
              onChange={(e) => setSelectedQuokka(e.target.value as 'F' | 'T')}
              className="flex flex-col gap-3 w-full"
              sx={{ width: '100%' }}
            >
              <FormControlLabel 
                value="F"
                control={
                  <Radio 
                    className="text-gray-300 checked:text-lime-500"
                    sx={{
                      color: 'grey.300',
                      '&.Mui-checked': {
                        color: 'lime.500',
                      },
                    }}
                  />
                } 
                label={
                  <div className="flex">
                    F Quokka
                  </div>
                }
                sx={{
                  margin: 0,
                  padding: '10px',
                  border: '2px solid',
                  borderRadius: '12px',
                  borderColor: selectedQuokka === 'F' ? 'lime.500' : 'grey.300',
                  backgroundColor: selectedQuokka === 'F' ? 'lime.100' : 'white',
                  width: '100%',
                }}
              />
              <FormControlLabel 
                value="T" 
                control={
                  <Radio 
                    className="text-gray-300 checked:text-lime-500"
                    sx={{
                      color: 'grey.300',
                      '&.Mui-checked': {
                        color: 'lime.500',
                      },
                    }}
                  />
                } 
                label={
                  <div className="flex items-center gap-2">
                    <span>T Quokka</span>
                  </div>
                }
                sx={{
                  margin: 0,
                  padding: '10px',
                  border: '2px solid',
                  borderRadius: '12px',
                  borderColor: selectedQuokka === 'T' ? 'lime.500' : 'grey.300',
                  backgroundColor: selectedQuokka === 'T' ? 'lime.100' : 'white',
                  width: '100%',
                }}
              />
            </RadioGroup>
          </FormControl>
        </div>

        {/* Start Button */}
        <div className="mt-auto">
          <Button
            fullWidth
            onClick={onComplete}
          >
            Start Journey
          </Button>
        </div>
      </div>
    </MobileContainer>
  )
}