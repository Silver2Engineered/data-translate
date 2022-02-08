import React from 'react';

const InputGroup = ({ label, children, ...props}) => (
  <div {...props}>
    <p style={{ margin: '0', fontSize: '1.3em' }}>
      { label }
    </p>
    { children }
  </div>
);

export default InputGroup;
